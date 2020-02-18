import numpy as np
from scipy.linalg import hadamard


# Перевод в двоичную систему
def to_bin(x, m):
    if x == 0:
        return '0'
    res = ''
    while x > 0:
        res = ('0' if x % 2 == 0 else '1') + res
        x //= 2

    b = [int(i) for i in res]
    while len(b) < m:
        b.insert(0, 0)

    return b


# Для кодирования
def mul_xor(a, b):
    res_mul = a * b
    ones = np.count_nonzero(res_mul)
    if ones % 2 == 0:
        out = 0
    else:
        out = 1

    return out


# Кодирование Рида-Маллера
def RM_encoding(message, m):
    message = np.array([int(i) for i in message], dtype=np.int)
    G_0_m = np.ones((1, 2 ** m), dtype=np.int)
    G_1_m = np.zeros((m, 2 ** m), dtype=np.int)
    for j in range(1, G_1_m.shape[1]):
        b_c = to_bin(j, m)
        G_1_m[:, j] = b_c

    # Порождающая матрица G
    G = np.vstack((G_0_m, G_1_m))

    # Кодирование
    code = []
    for j in range(G.shape[1]):
        b = G[:, j]
        c = mul_xor(message, b)
        code.append(c)

    return code


# Декодирование кода
def RM_decoding(code, m):
    # Полученное кодовое слово
    y = np.array(2 * np.array(code, dtype=int) - 1, dtype=np.int).reshape(1, 2 ** m)
    # Матрица Адамара
    h = hadamard(2 ** m)
    yh = y @ h

    # Поиск максимальное компоненты в результате умножения y на H
    k = np.argmax(np.abs(yh))
    # Ближайшее исправленное кодовое слово
    y_true = np.array((h[k, :] + 1) / 2, dtype=np.int)

    message = [y_true[0]]
    for i in range(m - 1, -1, -1):
        x = y_true[0] ^ y_true[2 ** i]
        message.append(x)

    return message


# Делаем ошибки в полеченном коде
def error(code, m):
    # Сколько можем исправить ошибок
    e = 2 ** (m - 2) - 1

    for i in range(e):
        k = np.random.randint(0, len(code) - 1)
        if code[k] == 1:
            code[k] = 0
        else:
            code[k] = 1

    print('Произведено {} ошибки'.format(e))

    return code


if __name__ == '__main__':
    message = str(input('Введите информационное слово:'))
    m = len(message) - 1

    # Кодирование
    code = RM_encoding(message, m)
    print('Закодированное сообщение:', np.array(code, dtype=np.int))

    # Ошибки
    code = error(code, m)
    print('Закодированное сообщение с ошибками:', np.array(code, dtype=np.int))

    # Декодирование
    x = RM_decoding(code, m)
    print('Исходное информационное слово', np.array(x, dtype=np.int))
