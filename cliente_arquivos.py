import socket
import os
import sys
import time

# Configurações do cliente
SERVIDOR_HOST = 'localhost'
SERVIDOR_PORT = 9600
BUFFER_SIZE = 1024
TAMANHO_FRAGMENTO = 1000
TIMEOUT = 1.0
MAX_TENTATIVAS = 10

# Tamanho de cada fragmento a ser enviado
# Timeout para retransmissão em segundos
# Número máximo de tentativas de retransmissão

# Criar socket UDP
try:
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error as e:
    print(f"Erro ao criar socket: {e}")
    sys.exit(1)


# Função para enviar arquivo
def enviar_arquivo(caminho_arquivo):
    # IMPLEMENTAR: Lógica para fragmentar e enviar arquivo
    # com confirmação de recebimento (ACKS)
    pass


# Função principal
def main():
    if len(sys.argv) != 2:
        print("Uso: python cliente_arquivos.py <caminho_do_arquivo>")
        sys.exit(1)

    caminho_arquivo = sys.argv[1]

    # Verificar se o arquivo existe
    if not os.path.isfile(caminho_arquivo):
        print(f"Erro: O arquivo '{caminho_arquivo}' não existe.")
        sys.exit(1)

    try:
        # Enviar solicitação inicial ao servidor
        nome_arquivo = os.path.basename(caminho_arquivo)
        solicitacao = f"ENVIAR: {nome_arquivo}"
        print(f"Solicitando envio de '{nome_arquivo}' para o servidor...")
        cliente.sendto(solicitacao.encode('utf-8'), (SERVIDOR_HOST, SERVIDOR_PORT))

        # Esperar confirmação do servidor
        cliente.settimeout(5.0)  # 5 segundos para timeout inicial
        try:
            resposta, _ = cliente.recvfrom(BUFFER_SIZE)
            if resposta.decode('utf-8') == "PRONTO":
                print("Servidor pronto para receber. Iniciando envio...")
                enviar_arquivo(caminho_arquivo)
            else:
                print(f"Resposta inesperada do servidor: {resposta.decode('utf-8')}")
        except socket.timeout:
            print("Timeout: O servidor não respondeu à solicitação inicial.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nCliente encerrado pelo usuário.")
    finally:
        cliente.close()
        print("Socket do cliente fechado.")


if __name__ == "__main__":
    main()
