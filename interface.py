from tkinter import *
import tkinter as tk
import threading
from connections.client import *

# Variáveis globais para armazenar os valores
mensagem = ""
tipo_codificacao = ""
opcao_modulacao = ""
opcoes = []

def enviar_mensagem():
    # Atualiza as variáveis globais com os valores dos widgets
    global mensagem, tipo_codificacao, opcao_modulacao
    mensagem = text_input.get()
    tipo_codificacao = cod.get()
    opcao_modulacao = modulacao.get()
    clientData = connect('transmissor')
    opcoes = [mensagem, tipo_codificacao]
    for opcao in opcoes:
        send(opcao,clientData)
    disconnect(clientData)

def interface_grafica():
    # Instância da janela
    window = Tk()
    window.title('Interface Gráfica')

    # Mensagem enviada
    label_input = Label(window, text="Digite a mensagem: ")
    label_input.grid(row=1)

    global text_input
    text_input = Entry(window)
    text_input.grid(row=1, column=1)

    # Variáveis para armazenar escolhas de codificação e modulação
    global cod, modulacao
    cod = tk.StringVar()
    modulacao = tk.StringVar()

    button_enviar = Button(window, text='Enviar', command=enviar_mensagem)
    button_enviar.grid(row=1, column=2)

    # Enquadramento
    enquadramento = tk.BooleanVar()  # Variável que armazena a escolha do enquadramento

    label_enq = Label(window, text="Enquadramento")
    label_enq.grid(row=2, column=0, padx=10)

    button_cont_caract = Radiobutton(window, text="Por contagem de caracter ", variable=enquadramento, value=True)
    button_cont_bits = Radiobutton(window, text="Por contagem de bits ", variable=enquadramento, value=False)

    button_cont_caract.grid(row=3, column=0, padx=10, pady=5)
    button_cont_bits.grid(row=4, column=0, padx=10, pady=5)

    # Codificação
    label_cod = Label(window, text='Codificação')
    label_cod.grid(row=2, column=2)

    button_NRZ = Radiobutton(window, text="NRZ", variable=cod, value='NRZ')
    button_Manch = Radiobutton(window, text="Manchester", variable=cod, value='Manchester')
    button_Bipolar = Radiobutton(window, text="Bipolar", variable=cod, value='Bipolar')

    button_NRZ.grid(row=3, column=2)
    button_Manch.grid(row=4, column=2)
    button_Bipolar.grid(row=5, column=2)

    # Modulação
    label_mod = Label(window, text='Modulação')
    label_mod.grid(row=6, column=0)

    label_ASK = Radiobutton(window, text="ASK", variable=modulacao, value='ASK')
    label_FSK = Radiobutton(window, text="FSK", variable=modulacao, value='FSK')
    label_8QM = Radiobutton(window, text="8QM", variable=modulacao, value='8QM')

    label_ASK.grid(row=7, column=0)
    label_FSK.grid(row=8, column=0)
    label_8QM.grid(row=9, column=0)

    return window.mainloop()
