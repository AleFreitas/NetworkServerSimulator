import socket
import threading
import pickle  # Adicionado para serialização/desserialização
import matplotlib.pyplot as plt
from carrier_modulation.ask import ask

HEADER = 64                                             #Tamanho padronizado da Mensagem
PORT = 5050                                             #Porta a ser utilizada
SERVER = socket.gethostbyname(socket.gethostname())     #Recebe o IP4 Local
ADDR = (SERVER, PORT)                                   #Endereço Completo
FORMAT = 'utf-8'                                        #Formato de Codificação
DISCONNECT_MESSAGE = 'DESCONECTOU'


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Instancia o servidor
server.bind(ADDR)                                           #Conecta com o endereço completo


def display_signal(signal,modulation):
    plt.plot(signal)
    plt.title(f"Sinal {modulation}")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.show()


def handle_client(conn, addr):
    print(f"Nova conexão: {addr}")

    connected = True
    while connected:
        # Recebe o tamanho da mensagem
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            # Recebe a mensagem de fato
            serialized_signal = conn.recv(msg_length)

            # Desserializa o sinal
            signal = pickle.loads(serialized_signal)

            print(f"Sinal recebido: {signal}")
            if(signal != DISCONNECT_MESSAGE):
                A = 1
                f = 10
                bitrate = 100
                display_signal(ask(A, f, signal, bitrate),'ASK')

    conn.close()

def start():
    server.listen()
    print(f"O servidor está ouvindo em {SERVER}:{PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Conexões Ativas {threading.active_count() - 1}")

print("Servidor está iniciando")
start()