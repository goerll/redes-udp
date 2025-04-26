import socket
import threading
import time
import sys

# Configurações do servidor
HOST = '0.0.0.0'  # Aceita conexões de qualquer IP
PORT = 9500  # Porta para o servidor escutar
BUFFER_SIZE = 1024
# Dicionário para armazenar os clientes conectados (endereço: nome)
clientes = {}


# Criar socket UDP
try:
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind((HOST, PORT))
    print(f"Servidor iniciado em {HOST}: {PORT}")
except socket.error as e:
    print(f"Erro ao criar socket: {e}")
    sys.exit(1)


# Função para enviar mensagem para todos os clientes
def broadcast(mensagem, endereco_origem=None):
    # IMPLEMENTAR: Enviar mensagem para todos os clientes exceto o de origem
    for endereco, nome in clientes.items():
        if endereco != endereco_origem:
            try:
                servidor.sendto(mensagem.encode('utf-8'), endereco)
            except Exception as e:
                print(f"Erro ao enviar mensagem para {nome}({endereco}): {e}")

# Loop principal do servidor
try:
    print("Aguardando mensagens...")
    while True:
        try:
            # Receber mensagem e endereço do cliente
            dados, endereco = servidor.recvfrom(BUFFER_SIZE)
            mensagem = dados.decode('utf-8')

            # Processar a mensagem recebida
            if mensagem.startswith('/registro:'):
                # IMPLEMENTAR: Registrar novo cliente
                nome = mensagem.split(':')[1].strip()
                clientes[endereco] = nome
                print(f"Novo cliente registrado: {nome}({endereco})")
                broadcast(f"Novo cliente registrado: {nome}({endereco})")
            elif mensagem.startswith('/sair'):
                # IMPLEMENTAR: Remover cliente que está saindo
                if endereco in clientes:
                    nome_cliente = clientes.pop(endereco)
                    print(f"Cliente {nome_cliente} ({endereco}) saiu.")
                    # Informa aos outros clientes sobre a saída
                    mensagem_saida = f"{nome_cliente} saiu do chat."
                    broadcast(mensagem_saida, endereco)
                else:
                    print(f"Recebido comando /sair de um cliente não registrado: {endereco}")
            else:
                # IMPLEMENTAR: Processar mensagem normal e fazer broadcast
                if endereco in clientes:
                    nome_cliente = clientes[endereco]
                    mensagem_com_nome = f"{nome_cliente}: {mensagem}"
                    print(f"Mensagem de {nome_cliente} ({endereco}): {mensagem}")
                    broadcast(mensagem_com_nome, endereco)
                else:
                    print(f"Mensagem de um cliente não registrado ({endereco}): {mensagem}")
                    mensagem_nao_registrado = "Você precisa se registrar usando /registro:<seu_nome> para enviar mensagens."
                    try:
                        servidor.sendto(mensagem_nao_registrado.encode('utf-8'), endereco)
                    except Exception as e:
                        print(f"Erro ao enviar mensagem de não registrado para {endereco}: {e}")
        except Exception as e:
            print(f"Erro no processamento da mensagem: {e}")
except KeyboardInterrupt:
    print("\nServidor encerrado pelo usuário.")
finally:
    servidor.close()
    print("Socket do servidor fechado.")
