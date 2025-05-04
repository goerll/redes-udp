import socket
import os
import time
import sys

# Configurações do servidor
HOST = '0.0.0.0'
PORT = 9600
BUFFER_SIZE = 1024
DIRETORIO_ARQUIVOS = './arquivos_recebidos/'

# Criar diretório para salvar arquivos se não existir
os.makedirs(DIRETORIO_ARQUIVOS, exist_ok=True)

# Criar socket UDP
try:
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind((HOST, PORT))
    print(f"Servidor UDP iniciado em {HOST}:{PORT}")
except socket.error as e:
    print(f"Erro ao criar socket: {e}")
    sys.exit(1)

# Função para receber arquivo
def receber_arquivo(nome_arquivo, endereco_cliente):
    caminho_arquivo = os.path.join(DIRETORIO_ARQUIVOS, nome_arquivo)
    arquivo = open(caminho_arquivo, 'wb')  # abre o arquivo para escrita binária

    esperado = 0  # número de sequência esperado
    tamanho_util = 0  # bytes escritos no arquivo (dados úteis)
    total_recebido = 0  # bytes recebidos no servidor (inclui retransmissões)
    retransmissoes = 0  # contador de retransmissões

    print(f"Recebendo arquivo {nome_arquivo}...")

    tempo_inicio = time.time()  # Marca o início da transferência

    while True:
        dados, endereco = servidor.recvfrom(BUFFER_SIZE)
        total_recebido += len(dados)  # soma tudo que chega, útil ou não

        # Verifica se é a mensagem de finalização
        if dados == b'FIM':
            tempo_fim = time.time()  # Marca o fim da transferência
            print(f"Arquivo {nome_arquivo} recebido com sucesso.")
            break

        # Extrai número de sequência (2 bytes) + dados
        num_seq = int.from_bytes(dados[:2], byteorder='big')  # os dois primeiros bytes são o número de sequência
        fragmento = dados[2:]

        if num_seq == esperado:
            # Se o fragmento é o esperado, escreve no arquivo
            arquivo.write(fragmento)
            tamanho_util += len(fragmento)  # soma dados úteis
            esperado += 1
            # Envia ACK para o cliente confirmando
            servidor.sendto(f"ACK:{num_seq}".encode('utf-8'), endereco_cliente)
        else:
            # Se não for o fragmento esperado, reenviar o último ACK
            retransmissoes += 1
            servidor.sendto(f"ACK:{esperado-1}".encode('utf-8'), endereco_cliente)

    arquivo.close()

    # Cálculos de tempo e taxa de transferência
    tempo_total = tempo_fim - tempo_inicio
    taxa_transferencia = (tamanho_util / 1024) / tempo_total  # KB/s

    # Cálculo de overhead (%)
    overhead = ((total_recebido - tamanho_util) / tamanho_util) * 100 if tamanho_util > 0 else 0

    # Imprime as informações formatadas
    print(f"Tamanho: {tamanho_util} bytes")
    print(f"Tempo: {tempo_total:.2f} segundos")
    print(f"Taxa de transferência: {taxa_transferencia:.2f} KB/s")
    print(f"Retransmissões: {retransmissoes}")
    print(f"Overhead: {overhead:.2f}%")

# Loop principal do servidor
try:
    print("Aguardando conexões...")
    while True:
        try:
            # Receber solicitação inicial
            dados, endereco = servidor.recvfrom(BUFFER_SIZE)
            mensagem = dados.decode('utf-8')

            # Se for uma solicitação de envio de arquivo
            if mensagem.startswith('ENVIAR:'):
                nome_arquivo = mensagem.split(':')[1]
                print(f"Nova conexão: {endereco}")

                # Enviar confirmação de pronto para receber
                servidor.sendto("PRONTO".encode('utf-8'), endereco)

                # Receber o arquivo
                receber_arquivo(nome_arquivo, endereco)

                print(f"Conexão fechada: {endereco}\n")

        except Exception as e:
            print(f"Erro: {e}")
except KeyboardInterrupt:
    print("\nServidor encerrado pelo usuário.")
finally:
    servidor.close()
    print("Socket do servidor fechado.")
