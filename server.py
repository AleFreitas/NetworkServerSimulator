import socket
import threading

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
        msg_lenght = conn.recv(HEADER).decode(FORMAT)   # Recebe o tamanho da mensagem
        if msg_lenght:
            msg_lenght = int(msg_lenght)
            msg = conn.recv(msg_lenght).decode(FORMAT)      # Recebe a mensagem de fato
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"{addr} {msg}")

    conn.close()

def start():
    server.listen()
    print(f"O servidor está ouvindo em {SERVER}")
    while True:
         conn, addr = server.accept()
         tread = threading.Thread(target=handle_client, args=(conn, addr))
         tread.start()
         print(f"Conexões Ativas {threading.active_count() - 1}")

print("Servidor está iniciando")
start()