import numpy as np
from const import S_BOX, N_ROWS, C_X, R_CON, N_ROUNDS, C_X_INV, S_BOX_INV
from utils import read_file, write_file, string_to_hex, string_to_block, code_to_string, mul, xor

N_S = 128  # длина блока (в битах)
N_K = 128  # длина ключа (в битах)

IN_MSG = 'input_msg.txt'
OUT_CODE = 'out_code.txt'
OUT_MSG = 'out_msg.txt'


# Замена state по s-box
def sub_bytes(s, inv=False):
    s_box = S_BOX_INV if inv else S_BOX
    res = []
    for row in s:
        l = []
        try:
            for el in row:
                n1 = el // 16
                n2 = el % 16
                l.append(s_box[n1][n2])
        except TypeError:
            n1 = row // 16
            n2 = row % 16
            res.append(s_box[n1][n2])
        else:
            res.append(l)
    return res


# Циклическое смещение строк state
def shift_rows(s, inv=False):
    for n_row in range(len(s)):
        for i in range(N_ROWS[N_S][n_row]):
            if inv:
                el = s[n_row].pop(-1)
                s[n_row].insert(0, el)
            else:
                el = s[n_row].pop(0)
                s[n_row].append(el)


# Смешивание столбцов state;
def mix_columns(s, inv=False):
    m = []
    c_x = C_X_INV if inv else C_X
    for j in range(len(s)):
        col = []
        for i in range(len(c_x)):
            sum = 0x00
            for k in range(len(c_x[0])):
                el = mul(s[k][j], c_x[i][k])
                sum = xor(int(sum), el)
            col.append(sum)
        m.append(col)
    for j in range(len(s)):
        for i in range(len(s)):
            s[i][j] = m[j][i]


# Сложение с раундовым ключом
def add_round_key(s, key):
    for i in range(len(s)):
        for j in range(len(s[0])):
            s[i][j] = s[i][j] ^ key[i][j]
    return np.transpose(s).tolist()


# Расширение ключа
def key_expansion(key):
    key = np.transpose(key).tolist()
    keys = [key]
    for i in range(N_ROUNDS[N_K][N_S]):
        col1 = keys[i][-1].copy()
        el = col1.pop(0)
        col1.append(el)
        col1 = sub_bytes(col1)
        key0 = keys[i][0]
        for j in range(len(key0)):
            try:
                col1[j] = col1[j] ^ key0[j] ^ R_CON[i%10][j]
            except TypeError:
                print('Вероятно, размер введённого ключа больше, чем указан в N_K')
                exit(1)
        round_key = [col1]
        for j in range(1, N_K // 32):
            col = []
            for k in range(len(key0)):
                col.append(round_key[j - 1][k] ^ keys[i][j][k])
            round_key.append(col)
        keys.append(round_key)
    return keys


# Функция шифрования
def encode(states, keys):
    rounds = N_ROUNDS[N_S][N_K]
    new_states = []
    for state in states:
        state_key = key_expansion(keys)
        s = add_round_key(np.transpose(state).tolist(), state_key[0])
        for i in range(rounds):
            s = sub_bytes(s)
            shift_rows(s)
            if i != rounds - 1:
                mix_columns(s)
            s = add_round_key(np.transpose(s).tolist(), state_key[i + 1])
        new_states.append(s)
    return new_states


# Функция дешифрования
def decode(states, keys):
    rounds = N_ROUNDS[N_S][N_K]
    new_states = []
    for state in states:
        state_key = key_expansion(keys)
        s = state.copy()
        for i in range(rounds):
            s = add_round_key(np.transpose(s).tolist(), state_key[-i - 1])
            if i != 0:
                mix_columns(s, True)
            shift_rows(s, True)
            s = sub_bytes(s, True)
        s = add_round_key(np.transpose(s).tolist(), state_key[0])
        new_states.append(s)
    return new_states


def main():
    message = read_file(IN_MSG)
    message_int = string_to_hex(message)
    message_block = string_to_block(message_int, N_S)

    key = input('Enter key: ')
    key_int = string_to_hex(key)
    key_block = string_to_block(key_int, N_K)

    message_code = encode(message_block, key_block)
    message_code_text = code_to_string(message_code)
    write_file(OUT_CODE, message_code_text)

    message_decode = decode(message_code, key_block)
    message_decode_text = code_to_string(message_decode)
    write_file(OUT_MSG, message_decode_text)


if __name__ == '__main__':
    main()
