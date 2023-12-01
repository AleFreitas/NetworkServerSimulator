import numpy as np

def ask(A, f, signal, bitrate):
    bit_duration = 1 / (2 * bitrate)  # Espaçamento de 1/2 segundo

    # Modulação ASK
    time_points = np.arange(0, len(signal) * bit_duration, bit_duration)
    ask_signal = [A * np.sin(2 * np.pi * f * t) if bit > 0 else 0 for t, bit in zip(time_points, signal)]
    return ask_signal
