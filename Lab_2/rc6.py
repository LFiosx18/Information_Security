import base64
import math

from utils import str_to_bin, bin_to_str, bin_expansion, shift, f, init_pq, read_file, write_to_file, print_result

IV = 'vector'
INPUT_MES = 'input_mes.txt'
OUTPUT_CODE = 'output_code.txt'
INPUT_CODE = OUTPUT_CODE
OUTPUT_MES = 'output_mes.txt'


def main():
    # w, r, secret_key = get_params()
    w, r, secret_key = 16, 20, 'test'

    message = read_file(INPUT_MES)
    bit_message = str_to_bin(message)
    while len(bit_message) % (w * 4) != 0:
        bit_message = '0' + bit_message

    bit_key = str_to_bin(secret_key)
    while len(bit_key) % w != 0:
        bit_key = '0' + bit_key

    len_key = len(bit_key) // 8
    c = int(8 * len_key / w)
    Pw, Qw = init_pq(w)

    # Конвертация секретного ключа
    L = []
    for i in range(c):
        L.append(int("0b" + bit_key[i:i + w], 2))

    # Инициализация массива ключей
    S = [Pw]
    for i in range(2 * r + 3):
        S.append((S[i] + Qw) % (2 ** w))

    # Перемешивание
    A = B = i = j = 0
    for cnt in range(3 * c):
        S[i] = shift((S[i] + A + B) % (2 ** w), 3, w, 'l')
        A = S[i]
        L[j] = shift((L[j] + A + B) % (2 ** w), (A + B) % (2 ** w), w, 'l')
        B = L[j]
        i = (i + 1) % (2 * r + 4)
        j = (j + 1) % c

    decoded_message = encryption(bit_message, w, S, r)
    write_to_file(OUTPUT_CODE, decoded_message)

    decoded_message_file = read_file(INPUT_CODE)
    encoded_message = decryption(decoded_message_file, w, S, r)
    write_to_file(OUTPUT_MES, base64.b64decode(bin_to_str(encoded_message)).decode('utf-8'))

    print_result(bit_message, decoded_message, encoded_message)


# Функция декодирования
def decryption(mes, w, S, r):
    result_bit = ''
    sync_pack = str_to_bin(IV)[:4 * w]
    while len(sync_pack) % (4 * w) != 0:
        sync_pack = '0' + sync_pack

    for i in range(0, len(mes), 4 * w):
        current_block = bin_expansion(mes[i: i + 4 * w], 4 * w)[2:]
        A = int('0b' + sync_pack[:w], 2)
        B = int('0b' + sync_pack[w:2 * w], 2)
        C = int('0b' + sync_pack[2 * w:3 * w], 2)
        D = int('0b' + sync_pack[3 * w:4 * w], 2)

        B = (B + S[0]) % (2 ** w)
        D = (D + S[1]) % (2 ** w)

        for j in range(r):
            t = shift(f(B, w), int(math.log(w, 10)), w, 'l')
            u = shift(f(D, w), int(math.log(w, 10)), w, 'l')
            A = (shift(A ^ t, u, w, 'l') + S[2 * (j + 1) + 1]) % (2 ** w)
            C = (shift(C ^ u, t, w, 'l') + S[2 * (j + 2) + 1]) % (2 ** w)

            A1, B1, C1, D1 = B, C, D, A
            A, B, C, D = A1, B1, C1, D1

        A = (A + S[2 * r + 2]) % (2 ** w)
        C = (C + S[2 * r + 3]) % (2 ** w)

        A = A ^ int('0b' + current_block[:w], 2)
        B = B ^ int('0b' + current_block[w:2 * w], 2)
        C = C ^ int('0b' + current_block[2 * w:3 * w], 2)
        D = D ^ int('0b' + current_block[3 * w:4 * w], 2)

        sync_pack = bin_expansion(bin(A), w)[2:] + bin_expansion(bin(B), w)[2:] + \
                    bin_expansion(bin(C), w)[2:] + bin_expansion(bin(D), w)[2:]
        result_bit += sync_pack
    return result_bit


# функция кодирования
def encryption(mes, w, S, r):
    result_bit = ''
    sync_pack = str_to_bin(IV)[:4 * w]
    while len(sync_pack) % (4 * w) != 0:
        sync_pack = '0' + sync_pack

    for i in range(0, len(mes), 4 * w):
        current_block = bin_expansion(mes[i: i + 4 * w], 4 * w)[2:]
        A = int('0b' + sync_pack[:w], 2)
        B = int('0b' + sync_pack[w:2 * w], 2)
        C = int('0b' + sync_pack[2 * w:3 * w], 2)
        D = int('0b' + sync_pack[3 * w:4 * w], 2)

        B = (B + S[0]) % (2 ** w)
        D = (D + S[1]) % (2 ** w)

        for j in range(r):
            t = shift(f(B, w), int(math.log(w, 10)), w, 'l')
            u = shift(f(D, w), int(math.log(w, 10)), w, 'l')
            A = (shift(A ^ t, u, w, 'l') + S[2 * (j + 1) + 1]) % (2 ** w)
            C = (shift(C ^ u, t, w, 'l') + S[2 * (j + 2) + 1]) % (2 ** w)

            A1, B1, C1, D1 = B, C, D, A
            A, B, C, D = A1, B1, C1, D1

        A = (A + S[2 * r + 2]) % (2 ** w)
        C = (C + S[2 * r + 3]) % (2 ** w)

        A = A ^ int('0b' + current_block[:w], 2)
        B = B ^ int('0b' + current_block[w:2 * w], 2)
        C = C ^ int('0b' + current_block[2 * w:3 * w], 2)
        D = D ^ int('0b' + current_block[3 * w:4 * w], 2)

        sync_pack = current_block

        result_bit += bin_expansion(bin(A), w)[2:] + bin_expansion(bin(B), w)[2:] + \
                      bin_expansion(bin(C), w)[2:] + bin_expansion(bin(D), w)[2:]

    return result_bit


if __name__ == '__main__':
    main()
