from tkinter import *
import tkinter as tk

def enviar_mensagem():
    mensagem = text_input.get()

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
    cod = tk.StringVar()

    label_cod = Label(window, text='Codificação')
    label_cod.grid(row=2, column=2)

    button_NRZ = Radiobutton(window, text="NRZ", variable=cod, value='NRZ')
    button_Manch = Radiobutton(window, text="Manchester", variable=cod, value='Manch')
    button_Bipolar = Radiobutton(window, text="Bipolar", variable=cod, value='Bipolar')

    button_NRZ.grid(row=3, column=2)
    button_Manch.grid(row=4, column=2)
    button_Bipolar.grid(row=5, column=2)

    # Modulação
    label_mod = Label(window, text='Modulação')
    label_mod.grid(row=6, column=0)

    label_ASK = Label(window, text="ASK")
    label_FSK = Label(window, text="FSK")
    label_8QM = Label(window, text="8QM")

    label_ASK.grid(row=7, column=0)
    label_FSK.grid(row=8, column=0)
    label_8QM.grid(row=9, column=0)

    return window.mainloop()

main()