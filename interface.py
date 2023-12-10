from tkinter import *
import tkinter as tk
from connections.client import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from globais import *
from threading import Thread
from bits import converter_mensagem_para_bits
import queue
def enviar_mensagem():
    # Atualiza as variáveis globais com os valores dos widgets
    bits_mensagem = converter_mensagem_para_bits(mensagem.get())
    opcoes.append(bits_mensagem)
    opcoes.append(cod.get())
    opcoes.append(modulacao.get())
    opcoes.append(erro.get())
    opcoes.append(erro_ad.get())
    clientData = connect("transmissor")
    for opcao in opcoes:
        send(opcao, clientData)
    disconnect(clientData)
def interface_grafica(bool):

    if bool == True:
        bool = False
        thread_server = threading.Thread(target=start, args=(serverData,))
        thread_server.start()

    # Instância da janela
    window = Tk()
    window.title('Interface Gráfica')

    # Mensagem enviada
    label_input = Label(window, text="Digite a mensagem:")
    label_input.grid(row=0, column=0, pady=5)

    global mensagem
    mensagem = Entry(window)
    mensagem.grid(row=0, column=1, pady=5)

    # Variáveis para armazenar escolhas de codificação e modulação
    global cod, modulacao
    cod = tk.StringVar()
    modulacao = tk.StringVar()
    
    global enquadramento
    enquadramento = tk.StringVar()
    
    global erro
    erro = tk.StringVar()

    global erro_ad
    erro_ad = tk.StringVar()

    button_enviar = Button(window, text='Enviar', command=enviar_mensagem)
    button_enviar.grid(row=0, column=2, pady=5)

    # Enquadramento
    enquadramento_frame = Frame(window)
    enquadramento_frame.grid(row=1, column=0, columnspan=3, pady=5)

    label_enq = Label(enquadramento_frame, text="Enquadramento")
    label_enq.grid(row=0, column=0, padx=10)

    button_cont_caract = Radiobutton(enquadramento_frame, text="Por contagem de caracter", variable=enquadramento,value=True)
    button_cont_bits = Radiobutton(enquadramento_frame, text="Por contagem de bits", variable=enquadramento,value=False)

    button_cont_caract.grid(row=1, column=0, padx=10, pady=5)
    button_cont_bits.grid(row=2, column=0, padx=10, pady=5)

    # Codificação
    label_cod = Label(window, text='Codificação')
    label_cod.grid(row=1, column=2, padx=10)

    button_NRZ = Radiobutton(window, text="NRZ", variable=cod, value='NRZ')
    button_Manch = Radiobutton(window, text="Manchester", variable=cod, value='Manchester')
    button_Bipolar = Radiobutton(window, text="Bipolar", variable=cod, value='Bipolar')

    button_NRZ.grid(row=2, column=2, padx=10)
    button_Manch.grid(row=3, column=2, padx=10)
    button_Bipolar.grid(row=4, column=2, padx=10)

    # Verificação de Erro
    label_erro = Label(window, text='Verificação de Erro')
    label_erro.grid(row=5, column=2, padx=10)

    button_PAR = Radiobutton(window, text="PAR", variable=erro, value='PAR')
    button_CRC = Radiobutton(window, text="CRC", variable=erro, value='CRC')

    button_PAR.grid(row=6, column=2, padx=10)
    button_CRC.grid(row=7, column=2, padx=10)

    #Adicionar Erro
    label_erro_ad = Label(window, text='Adicionar Erro?')
    label_erro_ad.grid(row=5, column=3, padx=10)

    button_ERRO_ad_S = Radiobutton(window, text="SIM", variable=erro_ad, value='SIM')
    button_ERRO_ad_S.grid(row=6, column=3, padx=10)
    button_ERRO_ad_N = Radiobutton(window, text="NAO", variable=erro_ad, value='NAO')
    button_ERRO_ad_N.grid(row=7, column=3, padx=10)

    # Modulação
    label_mod = Label(window, text='Modulação')
    label_mod.grid(row=1, column=0, padx=10)

    label_ASK = Radiobutton(window, text="ASK", variable=modulacao, value='ASK')
    label_FSK = Radiobutton(window, text="FSK", variable=modulacao, value='FSK')
    label_8QM = Radiobutton(window, text="8QM", variable=modulacao, value='8QM')

    label_ASK.grid(row=2, column=0, padx=10)
    label_FSK.grid(row=3, column=0, padx=10)
    label_8QM.grid(row=4, column=0, padx=10)

    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=8, column=0, columnspan=3, pady=10)

    return window.mainloop()


def handle_client(conn, addr, serverData):
    print('Nova Conexão!')
    connect = True
    while connect:
        msg_lenght = conn.recv(serverData['HEADER']).decode(serverData['FORMAT'])
        if msg_lenght:
            msg_lenght = int(msg_lenght)
            serialized_msg = conn.recv(msg_lenght)
            msg = pickle.loads(serialized_msg)
            if msg == serverData['DISCONNECT_MESSAGE']:
                connect = False
            else:
                message_queue.put(msg)
            print(f"{addr} {msg}")
    conn.close()

def start(serverData):
    serverData['server'].listen()
    print(f"O servidor está ouvindo em {serverData['ip']}")
    while True:
        conn, addr =  serverData['server'].accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, serverData))
        thread.start()
        print(f"Conexões Ativas {threading.active_count() - 2}")