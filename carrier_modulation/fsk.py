import numpy as np

def fsk(A, f1, f2, signal, opcao):
    """
        Recebe a amplitude A, a frequência da portadora para quando o bit é 1 -> f1,
        para quando o bit é 0 -> f2 e o sinal codificado.
        
        Retorna o sinal modulado em FSK.
    """
    signal_size = int(len(signal)/100)
    fsk_signal = np.zeros(signal_size * 100)

    if (opcao == 'NRZ') or (opcao == 'Manchester'):
        signal_to_bit_stream = []
        for i in range(signal_size):
            if (signal[i * 100 + 1] > 0):
                signal_to_bit_stream.append(1)
            else:
                signal_to_bit_stream.append(0)
    else:
        signal_to_bit_stream = []
        for i in range(signal_size):
            if (signal[i * 100 + 1] == 0):
                signal_to_bit_stream.append(0)
            else:
                signal_to_bit_stream.append(1)

    for i in range(signal_size):
        if int(signal_to_bit_stream[i]) == 1:
            for j in range(100):
                fsk_signal[i * 100 + j] = A * np.sin(2 * np.pi * f1 * j / 100)
        else:
            for j in range(100):
                fsk_signal[i * 100 + j] = A * np.sin(2 * np.pi * f2 * j / 100)

    return fsk_signal