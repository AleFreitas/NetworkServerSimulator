import numpy as np
import matplotlib.pyplot as plt

def nrz_polar(bits, amplitude):
    result = []
    for bit in bits:
        if int(bit) > 0:
            # cria uma lista com 100 elementos (amplitude) por bit
            # depois adiciona ao result
            # FORAM ESCOLHIDOS 100 DE CADA POR BIT DE FORMA TOTALMENTE ARBITRÁRIA
            # poderia ter sido feito só com result.extend([amplitude]) mas com
            # menos amostras o gráfico teria transições menos claras visualmente
            result.extend([amplitude] * 100)
        else:
            result.extend([-amplitude] * 100)
    return result

def fsk(A, f1, f2, bit_stream):
    sig_size = len(bit_stream)
    signal = np.zeros(sig_size * 100)

    for i in range(sig_size):
        if int(bit_stream[i]) == 1:
            for j in range(100):
                signal[(i-1) * 100 + j] = A * np.sin(2 * np.pi * f1 * j / 100)
        else:
            for j in range(100):
                signal[(i-1) * 100 + j] = A * np.sin(2 * np.pi * f2 * j / 100)

    return signal

# Exemplo de uso
A = 1
f1 = 1  # Frequência da portadora quando o bit é 0
f2 = 10  # Frequência da portadora quando o bit é 1
bit_stream = "01010011"
signal = nrz_polar(bit_stream, A)
fsk_signal = fsk(A, f1, f2, bit_stream)
# Plotagem do sinal nrz
plt.plot(signal)
plt.title("NRZ Polar")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.show()
# Plotagem do sinal fsk
plt.plot(fsk_signal)
plt.title("NRZ Polar")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.show()