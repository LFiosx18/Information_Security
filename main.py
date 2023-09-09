import re

REJEX = "^[а-яА-ЯёЁ ]+$"
FILE_NAME_INPUT_MES = 'input.txt'
FILE_NAME_OUTPUT_CODE = 'output.txt'
DICT1 = {'ё': 5, ' ': 32, ',': 33, '.': 34, '\n': 35, '-': 36, '!': 37, '?': 38, ':': 39, ';': 40}
DICT2 = {5: 'ё', 32: ' ', 33: ',', 34: '.', 35: '\n', 36: '-', 37: '!', 38: '?', 39: ':', 40: ';'}
N = 41


def read_keys():
    print("Enter the keys on a new line, press 'e' to complete the entry")
    key = input().lower()
    keys = []
    while key != '.':
        if re.compile(REJEX).search(key) is None:
            print("You should enter only russian symbols")
        else:
            keys.append(sym_to_num(key))
        key = input().lower()
    return keys


def read_message():
    with open(FILE_NAME_INPUT_MES, 'r', encoding='utf-8') as file:
        return file.read().lower()


def write_encrypted_message(message):
    with open(FILE_NAME_OUTPUT_CODE, 'w+', encoding='utf-8') as file:
        file.write(''.join(message))


def sym_to_num(message):
    codes = []
    for i in message:
        if i in DICT1:
            codes.append(DICT1[i])
            continue
        s = ord(i)
        if 1072 <= s <= 1103:
            codes.append(s - 1072)
    return codes


def num_to_sym(codes):
    message = []
    for i in codes:
        if i in DICT2:
            message.append(DICT2[i])
            continue
        message.append(chr(i + 1072))
    return message


def encryption(message, keys):
    message_code = sym_to_num(message)
    encryption_message = []
    for i in range(len(message_code)):
        res = message_code[i]
        for key in keys:
            res += key[i % len(key)]
        encryption_message.append(res % N)
    return num_to_sym(encryption_message)


def main():
    keys = read_keys()
    message = read_message()
    encryption_message = encryption(message, keys)
    write_encrypted_message(encryption_message)


if __name__ == '__main__':
    main()
