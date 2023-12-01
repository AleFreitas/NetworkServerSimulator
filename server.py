import socket
import threading
import pickle  # Adicionado para serialização/desserialização
import matplotlib.pyplot as plt

HEADER = 64                                             #Tamanho padronizado da Mensagem
PORT = 5050                                             #Porta a ser utilizada
SERVER = socket.gethostbyname(socket.gethostname())     #Recebe o IP4 Local
ADDR = (SERVER, PORT)                                   #Endereço Completo
FORMAT = 'utf-8'                                        #Formato de Codificação
DISCONNECT_MESSAGE = 'DESCONECTOU'


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Instancia o servidor
server.bind(ADDR)                                           #Conecta com o endereço completo


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

            # Faça o que precisar com o sinal, por exemplo, plotar
            print(f"Sinal recebido: {signal}")
            plt.plot(signal)
            plt.title("Sinal Recebido")
            plt.xlabel("Tempo (s)")
            plt.ylabel("Amplitude")
            plt.show()


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