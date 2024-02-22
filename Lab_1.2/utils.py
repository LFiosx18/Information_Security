import math
import numpy as np
from const import B


def read_file(file_name):
    with open(file_name, 'r', encoding="utf-8") as f:
        return f.read()


def write_file(file_name, text):
    with open(file_name, 'w+', encoding="utf-8") as f:
        f.write(text)


def string_to_block(msg, size):
    res = []
    rows = 4
    cols = math.ceil(size / 32)
    n = math.ceil(len(msg) / (cols * rows))
    for i in range(n):
        block = []
        for j in range(cols):
            col = []
            for k in range(rows):
                try:
                    col.append(msg[i * cols * rows + j * rows + k])
                except IndexError:
                    col.append(0)
            block.append(col)

        res.append(np.transpose(block).tolist())
    if len(res) == 1:
        return np.transpose(block).tolist()
    return res


def string_to_hex(msg):
    res = []
    for c in msg:
        sym = ord(c)
        if sym > 255:
            print('Invalid symbol: ' + c)
            exit(1)
        res.append(sym)
    return res


def code_to_string(blocks):
    string = ''
    for block in blocks:
        for row in np.transpose(block).tolist():
            for el in row:
                if el == 0:
                    return string
                string += chr(el)
    return string


def shift(n):
    c = bin(n) + '0'
    if len(c) > 10:
        return xor(int(c, 2), int(B))
    return int(c, 2)


def xor(x, y):
    res = x ^ y
    if len(bin(res)) > 10:
        return res ^ int(B)
    return res


def mul(a, b):
    if b == 0x01:
        return a
    if b == 0x02:
        return shift(a)
    if b == 0x03:
        return xor(shift(a), a)
    if b == 0x09:
        r_s = a
        for i in range(3):
            r_s = shift(r_s)
        return xor(r_s, a)
    if b == 0x0e or b == 0x0d:
        x_8 = a
        x_4 = a
        x_2 = a
        for i in range(3):
            x_8 = shift(x_8)
            if i == 1:
                x_4 = x_8
            if i == 0 and b == 0x0e:
                x_2 = x_8
        res = xor(x_8, x_4)
        return xor(res, x_2)
    if b == 0x0b:
        x_8 = a
        x_2 = a
        for i in range(3):
            x_8 = shift(x_8)
            if i == 0:
                x_2 = x_8
        res = xor(x_8, x_2)
        return xor(res, a)
