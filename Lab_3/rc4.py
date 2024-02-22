import copy

N = 16


def swap(a, b):
    return b, a


# Инициализация вектора перестановок
def init_s(key):
    s = [i for i in range(2 ** N)]  # 2 ** N
    key_l = len(key)
    j = 0
    for i in range(2 ** N):  # 2 ** N
        j = (j + s[i] + key[i % key_l]) % 2 ** N  # 2 ** N
        s[i], s[j] = swap(s[i], s[j])
    return s


# Генератор псевдо-случайной последовательности
def generator(s, i, j):
    i = (i + 1) % 2 ** N  # 2 ** N
    j = (j + s[i]) % 2 ** N  # 2 ** N
    s[i], s[j] = swap(s[i], s[j])
    t = (s[i] + s[j]) % 2 ** N
    k = s[t]
    return s, i, j, k


def string_to_bin(string):
    res = []
    for c in string:
        c_bin = format(ord(c), 'b')
        while len(c_bin) != 8:
            c_bin = '0' + c_bin
        res.append('0b' + c_bin)
    return res


def bin_to_string(bin_array):
    res = ''
    for i in bin_array:
        if len(i) <= 10:
            size = 10
        else:
            size = 18
        while len(i) != size:
            i = i[:2] + '0' + i[2:]
        i1 = int(i[:10], 2)
        res += chr(i1)
        if size == 18:
            i2 = int('0b' + i[10:], 2)
            res += chr(i2)

    return res


def string_to_int(string):
    res = []
    for c in string:
        c_bin = format(ord(c), 'b')
        res.append(int(c_bin, 2))
    return res


def int_to_bin(num):
    res = bin(num)
    while len(res) != 18:
        res = res[:2] + '0' + res[2:]
    return res


# Функция кодирования
def encode(s, msg):
    res = []
    i, j = 0, 0
    for c_i in range(0, len(msg), 2):
        current_byte_1 = string_to_bin(msg[c_i])[0]
        try:
            current_byte_2 = string_to_bin(msg[c_i + 1])[0]
            current_bytes = current_byte_1 + current_byte_2[2:]
        except IndexError:
            current_bytes = current_byte_1
        s, i, j, k = generator(s, i, j)
        k_bin = int_to_bin(k)
        res.append(str(bin(int(current_bytes, 2) ^ int(k_bin, 2))))

    return res


# Функция декодирования
def decode(msg, s):
    res = []
    msg = string_to_bin(msg)
    i, j = 0, 0
    for c_i in range(0, len(msg), 2):
        s, i, j, k = generator(s, i, j)
        k_bin = int_to_bin(k)
        current_byte_1 = msg[c_i]
        try:
            current_byte_2 = msg[c_i + 1]
            current_bytes = current_byte_1 + current_byte_2[2:]
        except IndexError:
            current_bytes = current_byte_1
        res.append(str(bin(int(current_bytes, 2) ^ int(k_bin, 2))))
    return res


def main():
    key = 'D685kjgb56'
    message = 'Hello, world! 73'
    s = init_s(string_to_int(key))
    s1 = copy.deepcopy(s)
    message_coded = encode(s, message)
    result_coded = bin_to_string(message_coded)
    print(f'Result coded:\n{result_coded}\n\n')

    message_decoded = decode(result_coded, s1)
    result_decoded = bin_to_string(message_decoded)
    print(f'Result decoded:\n{message_decoded}\n\n')
    print(f'Result decoded text:\n{result_decoded}\n\n')


if __name__ == '__main__':
    main()
