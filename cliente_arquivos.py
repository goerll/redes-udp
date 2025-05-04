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

# Criar socket UDP
try:
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error as e:
    print(f"Erro ao criar socket: {e}")
    sys.exit(1)

# Função para enviar arquivo
def enviar_arquivo(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'rb') as arquivo:
            dados = arquivo.read()

        total_fragmentos = (len(dados) + TAMANHO_FRAGMENTO - 1) // TAMANHO_FRAGMENTO
        num_seq = 0

        print(f"Arquivo com {len(dados)} bytes será enviado em {total_fragmentos} fragmentos.")

        cliente.settimeout(TIMEOUT)

        while num_seq < total_fragmentos:
            # Define os limites do fragmento
            inicio = num_seq * TAMANHO_FRAGMENTO
            fim = inicio + TAMANHO_FRAGMENTO
            fragmento = dados[inicio:fim]

            # Cria pacote: 2 bytes para o número de sequência + fragmento
            pacote = num_seq.to_bytes(2, byteorder='big') + fragmento

            tentativas = 0
            enviado = False

            while not enviado and tentativas < MAX_TENTATIVAS:
                try:
                    cliente.sendto(pacote, (SERVIDOR_HOST, SERVIDOR_PORT))
                    resposta, _ = cliente.recvfrom(BUFFER_SIZE)
                    resposta = resposta.decode('utf-8')

                    if resposta.startswith('ACK:'):
                        ack_num = int(resposta.split(':')[1])
                        if ack_num == num_seq:
                            print(f"Fragmento {num_seq} enviado e confirmado.")
                            enviado = True
                            num_seq += 1
                        else:
                            print(f"ACK inesperado: {ack_num}. Esperado: {num_seq}. Reenviando...")
                    else:
                        print(f"Resposta inesperada: {resposta}. Reenviando fragmento {num_seq}...")
                except socket.timeout:
                    tentativas += 1
                    print(f"Timeout esperando ACK do fragmento {num_seq}. Tentativa {tentativas}/{MAX_TENTATIVAS}.")

            if not enviado:
                print(f"Falha ao enviar fragmento {num_seq} após {MAX_TENTATIVAS} tentativas.")
                return

        # Após enviar todos os fragmentos, enviar sinal de fim
        cliente.sendto(b'FIM', (SERVIDOR_HOST, SERVIDOR_PORT))
        print("Arquivo enviado com sucesso!")

    except Exception as e:
        print(f"Erro ao enviar arquivo: {e}")

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
        solicitacao = f"ENVIAR:{nome_arquivo}"
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
