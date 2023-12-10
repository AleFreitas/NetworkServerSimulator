import numpy as np

def ask(A, f1, f2, signal):
    """
    Recebe a amplitude A, a frequência da portadora f e o sinal codificado.
    
    Retorna o sinal modulado em ASK.
    """
    signal_size = int(len(signal)/100)
    ask_signal = np.zeros(signal_size * 100)

    signal_to_bit_stream = []
    for i in range(signal_size):
        if(signal[i*100+1] > 0):
            signal_to_bit_stream.append(1)
        else:
            signal_to_bit_stream.append(0)

    for i in range(signal_size):
        if signal_to_bit_stream[i] == 1:
            for j in range(1, 101):
                ask_signal[i * 100 + j - 1] = A * np.sin(2 * np.pi * f * j / 100)
        else:
            for j in range(1, 101):
                ask_signal[i * 100 + j - 1] = 0

    return ask_signal
