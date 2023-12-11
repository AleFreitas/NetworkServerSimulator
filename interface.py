from tkinter import *
import tkinter as tk
from connections.client import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from globais import *
from threading import Thread
from bits import *
from carrier_modulation.ask import *
from carrier_modulation.fsk import *

ax_digital = None  # Garante que 'ax' seja global
canvas_digital = None

ax_mod = None  # Garante que 'ax' seja global
canvas_mod = None

text_box = None
text_box1 = None
text_box2 = None

encoding_mod = {
        'ASK': ask,
        'FSK': fsk,
    }

def enviar_mensagem():
    global bits_mensagem
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

def atualizar_graficos():

    global bits_mensagem, ax_digital, ax_modx

    for item in bits_mensagem:
        text_box.insert(END, f"{item}")         # Escreve os Bits da Mensagem Original

    text_box.insert(END, f"\n")
    text_box.insert(END, f"{mensagem.get()}")   # Escreve a mensagem original

    for item1 in informacoes[1]:                # Escreve os Bits recebidos
        text_box1.insert(END, f"{item1}")

    recebido = converter_bits_para_mensagem(informacoes[1])     # Transforma os Bits da mensagem recebida para msg

    print(recebido)
    text_box1.insert(END, f"\n")
    text_box1.insert(END, f"{recebido}")         # Escreve a mensagem recebida

    for item2 in informacoes[2]:
        text_box2.insert(END, f"{item2}")       # Escreve se houve erro

    # Atualize os gráficos
    ax_digital.clear()
    ax_digital.plot(informacoes[0])
    ax_digital.set_title(opcoes[1])
    ax_digital.set_xlabel("Tempo(s)")
    ax_digital.set_ylabel("Amplitude")

    # Atualize a tela da interface gráfica
    canvas_digital.draw()

    ax_mod.clear()
    sinal = encoding_mod[opcoes[2]](1 ,1, 3, informacoes[0],opcoes[1])
    ax_mod.plot(sinal)
    ax_mod.set_title(opcoes[2])
    ax_mod.set_xlabel("Tempo(s)")
    ax_mod.set_ylabel("Amplitude")

    # Atualize a tela da interface gráfica
    canvas_mod.draw()


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

    button_enviar = Button(window, text='Atualizar', command=atualizar_graficos)
    button_enviar.grid(row=0, column=3, pady=5)

    # Enquadramento
    label_enq = Label(window, text='Enquadramento')
    label_enq.grid(row=2, column=1, padx=3, pady=10)

    button_cont_caract = Radiobutton(window, text="Por contagem de caracter", variable=enquadramento, value=True)
    button_cont_bits = Radiobutton(window, text="Por contagem de bits", variable=enquadramento, value=False)

    button_cont_caract.grid(row=3, column=1, pady=5)
    button_cont_bits.grid(row=4, column=1, pady=5)

    # Codificação
    label_cod = Label(window, text='Codificação')
    label_cod.grid(row=2, column=2, padx=3, pady=10)  # Adicionei pady aqui

    button_NRZ = Radiobutton(window, text="NRZ", variable=cod, value='NRZ')
    button_Manch = Radiobutton(window, text="Manchester", variable=cod, value='Manchester')
    button_Bipolar = Radiobutton(window, text="Bipolar", variable=cod, value='Bipolar')

    button_NRZ.grid(row=3, column=2, pady=5)
    button_Manch.grid(row=4, column=2, pady=5)
    button_Bipolar.grid(row=5, column=2, pady=5)

    # Verificação de Erro
    label_erro = Label(window, text='Verificação de Erro')
    label_erro.grid(row=2, column=3, padx=3, pady=10)  # Adicionei pady aqui

    button_PAR = Radiobutton(window, text="PAR", variable=erro, value='PAR')
    button_CRC = Radiobutton(window, text="CRC", variable=erro, value='CRC')

    button_PAR.grid(row=3, column=3, pady=5)
    button_CRC.grid(row=4, column=3, pady=5)

    # Adicionar Erro
    label_erro_ad = Label(window, text='Adicionar Erro?')
    label_erro_ad.grid(row=2, column=4, padx=3, pady=10)  # Adicionei pady aqui

    button_ERRO_ad_S = Radiobutton(window, text="SIM", variable=erro_ad, value='SIM')
    button_ERRO_ad_S.grid(row=3, column=4, pady=5)
    button_ERRO_ad_N = Radiobutton(window, text="NAO", variable=erro_ad, value='NAO')
    button_ERRO_ad_N.grid(row=4, column=4, pady=5)

    # Modulação
    label_mod = Label(window, text='Modulação')
    label_mod.grid(row=2, column=0, padx=3, pady=10)  # Adicionei pady aqui

    label_ASK = Radiobutton(window, text="ASK", variable=modulacao, value='ASK')
    label_FSK = Radiobutton(window, text="FSK", variable=modulacao, value='FSK')
    label_8QM = Radiobutton(window, text="8QM", variable=modulacao, value='8QM')

    label_ASK.grid(row=3, column=0, pady=5)
    label_FSK.grid(row=4, column=0, pady=5)
    label_8QM.grid(row=5, column=0, pady=5)


    # Gráfico Digital
    global ax_digital, canvas_digital
    fig_digital, ax_digital = plt.subplots(figsize=(5, 4), dpi=100)
    canvas_digital = FigureCanvasTkAgg(fig_digital, master=window)
    canvas_widget_digital = canvas_digital.get_tk_widget()
    canvas_widget_digital.grid(row=8, column=0, columnspan=2, pady=10)
    ax_digital.set_title("Indefinido")
    ax_digital.set_xlabel("Tempo(s)")
    ax_digital.set_ylabel("Amplitude")

    # Gráfico de Modulação
    global ax_mod, canvas_mod
    fig_mod, ax_mod = plt.subplots(figsize=(5, 4), dpi=100)
    canvas_mod = FigureCanvasTkAgg(fig_mod, master=window)
    canvas_widget_mod = canvas_mod.get_tk_widget()
    canvas_widget_mod.grid(row=8, column=4, columnspan=2, pady=10)
    ax_mod.set_title("Indefinido")
    ax_mod.set_xlabel("Tempo(s)")
    ax_mod.set_ylabel("Amplitude")

    global text_box, text_box1, text_box2
    label_msg = Label(window, text='Mensagem Original')
    label_msg.grid(row=0, column=5, padx=3, pady=5)  # Adicionei pady aqui
    text_box = Text(window, height=2, width=30)
    text_box.grid(row=1, column=5, padx=3, pady=5)

    label_msg1 = Label(window, text='Mensagem Recebida')
    label_msg1.grid(row=2, column=5, padx=3, pady=5)  # Adicionei pady aqui
    text_box1 = Text(window, height=2, width=30)
    text_box1.grid(row=3, column=5, padx=3, pady=5)

    label_msg2 = Label(window, text='Houve Erro?')
    label_msg2.grid(row=4, column=5, padx=3, pady=5)  # Adicionei pady aqui
    text_box2 = Text(window, height=2, width=30)
    text_box2.grid(row=5, column=5, padx=3, pady=5)

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
                informacoes.append(msg)
            print(f"{addr} {msg}")
    conn.close()

def start(serverData):
    serverData['server'].listen()
    print(f"O servidor está ouvindo em {serverData['ip']}")
    while len(informacoes) != 3:
        conn, addr =  serverData['server'].accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, serverData))
        thread.start()
        print(f"Conexões Ativas {threading.active_count() - 2}")