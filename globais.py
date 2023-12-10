# Variáveis globais para armazenar os valores
import socket
import queue

opcoes = []
bits_mensagem = []
HEADER = 64
PORT = 5052
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "Desconectar"
FORMAT = "utf-8"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
serverData = {"HEADER": HEADER, "FORMAT": FORMAT, "server": server, "ip": SERVER, "DISCONNECT_MESSAGE": DISCONNECT_MESSAGE}
message_queue = queue.Queue()
informacoes = []   # Indice 1: Sinal Digital // Indice 2: Bits de Mensagem // Indice 3: Existência de # Erro

