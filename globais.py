# Bibliotecas Utilizadas
import socket

# Variáveis Globais Utilizadas

# Variáveis de Armazenamento dos Resultados
opcoes = []
bits_mensagem = []
informacoes = []   # Indice 0: Sinal Digital // Indice 1: Bits de Mensagem // Indice 2: Existência de # Erro


# Variáveis de Configuração do Servidor realizado dentro da Interface Gráfica
HEADER = 64
PORT = 5052
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "Desconectar"
FORMAT = "utf-8"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
serverData = {"HEADER": HEADER, "FORMAT": FORMAT, "server": server, "ip": SERVER, "DISCONNECT_MESSAGE": DISCONNECT_MESSAGE}

