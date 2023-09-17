import re

REJEX = "^[а-яА-ЯёЁ ]+$"                # Регулярное выражение для проверки ключей на валидность
FILE_NAME_INPUT_MES = 'Lab_1/input.txt'
FILE_NAME_OUTPUT_CODE = 'Lab_1/output.txt'
FILE_NAME_INPUT_CODE = 'Lab_1/output.txt'
FILE_NAME_OUTPUT_MES = 'Lab_1/output2.txt'

# Дополнительные символы алфавита
DICT1 = {'ё': 32, ' ': 33, ',': 34, '.': 35, '\n': 36, '-': 37, '!': 38, '?': 39, ':': 40, ';': 41}
DICT2 = {32: 'ё', 33: ' ', 34: ',', 35: '.', 36: '\n', 37: '-', 38: '!', 39: '?', 40: ':', 41: ';'}
N = 42                                  # Мощность используемого алфавита


# Чтение ключей и проверка их на отсутствие запрещённых символов
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


# Чтение файла с сообщением
def read_message(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read().lower()


# Запись сообщения в файл
def write_message(file_name, message):
    with open(file_name, 'w+', encoding='utf-8') as file:
        file.write(''.join(message))


# Преобразование символов в числовое представление
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


# Преобразование числа в соответствующий ему символ алфавита
def num_to_sym(codes):
    message = []
    for i in codes:
        if i in DICT2:
            message.append(DICT2[i])
            continue
        message.append(chr(i + 1072))
    return message


# Шифрование
def encryption(message, keys):
    message_code = sym_to_num(message)
    encryption_message = []
    for i in range(len(message_code)):
        res = message_code[i]
        for key in keys:
            res += key[i % len(key)]
        encryption_message.append(res % N)
    return num_to_sym(encryption_message)


# Дешифрование
def decryption(message, keys):
    message_code = sym_to_num(message)
    decryption_message = []
    for i in range(len(message_code)):
        res = message_code[i]
        for key in keys:
            res -= key[i % len(key)]
        decryption_message.append(res % N)
    return num_to_sym(decryption_message)


def main():
    keys = read_keys()                                          # Чтение ключей
    message = read_message(FILE_NAME_INPUT_MES)                 # Чтение исходного сообщения
    encryption_message = encryption(message, keys)              # Шифрование сообщения
    write_message(FILE_NAME_OUTPUT_CODE, encryption_message)    # Запись результата в файл

    new_key = input('New keys?\n')
    if new_key == 'y':
        keys = read_keys()
    message = read_message(FILE_NAME_INPUT_CODE)                # Чтение зашифрованного сообщения
    decryption_message = decryption(message, keys)              # Дешифрование сообщения
    write_message(FILE_NAME_OUTPUT_MES, decryption_message)     # Запись результата в файл


if __name__ == '__main__':
    main()
