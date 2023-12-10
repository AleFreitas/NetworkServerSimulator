def converter_bits_para_mensagem(bits):
    # Agrupa os bits em grupos de 8 para obter os caracteres originais
    caracteres = [bits[i:i+8] for i in range(0, len(bits), 8)]

    # Converte cada grupo de 8 bits de volta para um caractere
    mensagem = ''.join([chr(int(''.join(map(str, grupo)), 2)) for grupo in caracteres])

    return mensagem

def converter_mensagem_para_bits(mensagem):
    # Converte cada caractere da mensagem para sua representação binária
    bits_mensagem = []
    for char in mensagem:
        bits_char = bin(ord(char))[2:].zfill(8)  # Obtém a representação binária de cada caractere
        bits_mensagem.extend(map(int, list(bits_char)))  # Adiciona os bits à lista

    return bits_mensagem