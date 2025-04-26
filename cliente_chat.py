import socket
import threading
import sys
import time

# Configurações do cliente
SERVIDOR_HOST = 'localhost'  # Endereço do servidor
SERVIDOR_PORT = 9500  # Porta do servidor
BUFFER_SIZE = 1024

# Criar socket UDP
try:
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error as e:
    print(f"Erro ao criar socket: {e}")
    sys.exit(1)


# Função para receber mensagens.
def receber_mensagens():
    # IMPLEMENTAR: Função que recebe mensagens do servidor continuamente
    while True:
        try:
            dados, endereco_servidor = cliente.recvfrom(BUFFER_SIZE)
            mensagem = dados.decode('utf-8')
            print(mensagem)
        except socket.error as e:
            print(f"Erro ao receber mensagem: {e}")
            break
        except KeyboardInterrupt:
            break


# Registrar usuário no servidor
def registrar_usuario(nome):
    mensagem_registro = f"/registro:{nome}"
    try:
        cliente.sendto(mensagem_registro.encode('utf-8'), (SERVIDOR_HOST, SERVIDOR_PORT))
    except socket.error as e:
        print(f"Erro ao enviar mensagem de registro: {e}")

# Função principal
def main():
    if len(sys.argv) != 2:
        print("Uso: python cliente_chat.py <seu_nome>")
        sys.exit(1)

    nome_usuario = sys.argv[1]

    try:
        # Registrar no servidor
        registrar_usuario(nome_usuario)

        # Iniciar thread para receber mensagens
        thread_recebimento = threading.Thread(target=receber_mensagens)
        thread_recebimento.daemon = True
        thread_recebimento.start()

        print(f"Conectado ao servidor. Digite '/sair' para encerrar.")

        # Loop principal para enviar mensagens
        while True:
            mensagem = input()
            if mensagem.lower() == '/sair':
                # IMPLEMENTAR: Enviar comando de saida e encerrar cliente
                mensagem_saida = '/sair'
                try:
                    cliente.sendto(mensagem_saida.encode('utf-8'), (SERVIDOR_HOST, SERVIDOR_PORT))
                except socket.error as e:
                    print(f"Erro ao enviar comando de saída: {e}")
                break
            else:
                try:
                    mensagem_completa = mensagem.encode('utf-8')
                    cliente.sendto(mensagem_completa, (SERVIDOR_HOST, SERVIDOR_PORT))
                except socket.error as e:
                    print(f"Erro ao enviar mensagem: {e}")
    except KeyboardInterrupt:
        print("\nCliente encerrado pelo usuário.")
    finally:
        cliente.close()
        print("Socket do cliente fechado.")


if __name__ == "__main__":
    main()
