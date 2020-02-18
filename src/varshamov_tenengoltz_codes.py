import numpy as np


# Генерация кодов Варшамова-Тенегольца
def generate_vt_codes(n):
    module = n + 1
    b = []
    for i in range(n ** 2):
        b.append(bin(i)[2:].zfill(n))

    sum_of_numbers = []
    for numbers in b:
        sum_of_numbers.append(get_S(numbers))

    vt_codes = []
    for i in range(len(sum_of_numbers)):
        if sum_of_numbers[i] % module == 0:
            vt_codes.append(b[i])

    return vt_codes


# Сумма по формуле
def get_S(word):
    word = to_list(word)
    s = 0

    for i in range(len(word)):
        s += (i + 1) * word[i]

    return s


# Весл слова
def weight(word):
    word = to_list(word)
    w = 0

    for i in range(len(word)):
        if word[i] == 1:
            w += 1

    return w


# Выпадение символа
def bit_loss(word):
    word = to_list(word)
    k = np.random.randint(0, len(word) - 1)
    print('Потерянный символ:', word[k])
    word.pop(k)

    return word


# Исправление ошибки выпадения символа
def bit_loss_correction(word):
    s = get_S(word)
    w = weight(word)
    module = len(word) + 2
    t = -s % module

    n = len(word) + 1

    if t <= w:
        k = 0
        for i in range(len(word) - 1, -1, -1):
            if word[i] == 1:
                k += 1
            if k == t:
                word.insert(i, 0)
                break
    else:
        k = 0
        for i in range(len(word) - 1, -1, -1):
            if word[i] == 0:
                k += 1
            if k == n - t:
                word.insert(i, 1)
                break

    return word


# Вставка символа
def insert_bit(word):
    word = to_list(word)
    k = np.random.randint(0, len(word) - 1)
    # Вставляем случайно 0 или 1 в случайную позицию k
    b = np.random.randint(0, 2)
    print('Вставленный символ:', b)
    word.insert(k, b)

    return word


# Исправление ошибки вставки символа
def insert_bit_correction(word):
    s = get_S(word)
    w = weight(word)
    module = len(word)
    t = s % module

    if t == 0:
        word.pop(len(word - 1))
    elif t == w:
        word.pop(0)
    else:
        if t < w:
            n1 = t
            k = 0
            for i in range(len(word) - 1, -1, -1):
                if word[i] == 1:
                    k += 1
                if k == n1 and word[i] == 0:
                    word.pop(i)
                    break
        else:
            n0 = len(word) - t
            k = 0
            for i in range(len(word) - 1, -1, -1):
                if word[i] == 0:
                    k += 1
                if k == n0 and word[i] == 1:
                    word.pop(i)
                    break

    return word


def make_bit_error(word):
    word = to_list(word)
    k = np.random.randint(0, len(word))
    if word[k] == 0:
        word[k] = 1
    else:
        word[k] = 0

    print('На {} позиции бит изменился на {}'.format(k + 1, word[k]))
    print('Код с искажённым битом:', word)

    return word


def invariance_correction(word):
    word = to_list(word)
    s = get_S(word)
    w = weight(word)
    module = len(word) + 1
    t = s % module

    # Correction process
    if word[t - 1] == 0:
        word[-t] = 1
        return word
    else:
        word[t - 1] = 0
        return word


def to_list(x):
    x = [int(i) for i in x]
    return x


if __name__ == '__main__':
    n = 7
    vt_codes = generate_vt_codes(n)
    print('Коды Варшамова-Тененгольца:', vt_codes)

    word = vt_codes[np.random.randint(0, len(vt_codes) - 1)]
    print('Слово:', word)

    # Выпадение символа
    lost_word = bit_loss(word)
    print('Слово в результате выпадения символа:', lost_word)

    correction_lost_word = bit_loss_correction(lost_word)
    print('Исправленная ошибка выпадения символа:', correction_lost_word)

    print('------------------------------------------------------')

    # Вставка символа
    inserted_word = insert_bit(word)
    print('Слово в результате вставки символа:', inserted_word)

    correction_inserted_word = insert_bit_correction(word)
    print('Исправленная ошибка вставки символа:', correction_inserted_word)

    print('------------------------------------------------------')

    # Ошибка в бите и испрввление
    err_word = make_bit_error(word)
    correct_word = invariance_correction(err_word)
    print('Исправленное искажение бита:', correct_word)
