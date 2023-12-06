import base64
import math

E = 2.71828
FI = 1.61803


def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()


def write_to_file(file_name, message):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(message)


def get_params():
    param_w = 0
    while param_w not in [16, 32, 64]:
        try:
            param_w = int(input('Размер слова в битах (16, 32, 64): '))
        except ValueError:
            pass

    param_r = -1
    while not 0 <= param_r <= 255:
        try:
            param_r = int(input('Количество раундов (от 0 до 255): '))
        except ValueError:
            pass

    param_secret_key = ''
    while param_secret_key == '':
        param_secret_key = input('Секретный ключ: ')

    return param_w, param_r, param_secret_key


def bin_expansion(bit_string, length):
    if bit_string.startswith('0b'):
        while len(bit_string) != length + 2:
            bit_string = bit_string[:2] + '0' + bit_string[2:]
    else:
        while len(bit_string) != length:
            bit_string = '0' + bit_string
        return '0b' + bit_string

    return bit_string


def str_to_bin(str):
    str_bytes = bytearray(base64.b64encode(bytes(str, 'utf-8')))
    res_list = []
    for byte in str_bytes:
        res_list.append(bin_expansion(bin(byte), 8)[2:])

    return ''.join(res_list)


def bin_to_str(bin_mes):
    output = [int('0b' + bin_mes[block * 8: (block + 1) * 8], 2) for block in range(int(len(bin_mes) / 8))]
    output = bytes(output)
    return output


def init_pq(w):
    p = math.floor((E - 2) * (2 ** w))
    q = math.floor((FI - 1) * (2 ** w))

    if p % 2 == 0:
        p += 1

    if q % 2 == 0:
        q += 1

    return p, q


def shift(num, bits, w, mode):
    num = bin_expansion(bin(num), w)[2:]
    bits %= w
    if mode == 'l':
        return int('0b' + num[bits:] + num[:bits], 2)
    else:
        return int('0b' + num[-bits:] + num[:-bits], 2)


def f(x, w):
    return (x * (2 * x + 1)) % (2 ** w)


DEFAULT = '\033[37m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
VIOLET = '\033[35m'


def print_result(message_bin, decoded_mes, encoded_mes):
    print((YELLOW + 'Исходное сообщение:' + DEFAULT))
    print(message_bin + '\n')
    print(GREEN + 'Закодированное сообщение:' + DEFAULT)
    print(decoded_mes + '\n')
    print(VIOLET + 'Декодированное сообщение:' + DEFAULT)
    print(encoded_mes + '\n')
