# from random import choice


# def file_processing(path):
#     res = []
#     del_all_refs(path)
#
#     with open(path, encoding='utf8') as text:
#         for line in text:
#             if line.rstrip():
#                 words = line.split()
#
#                 word_f = choice(words)
#                 word_f_ind = words.index(word_f)
#
#                 # Чтоб word_f не было последним и не было кривым
#                 while word_f_ind > len(words) - 1 and word_f in ['-', '—'] and len(word_f) < 3 and word_f.isdigit():
#                     word_f = choice(words)
#                     word_f_ind = words.index(word_f)
#
#                 word_s = words[word_f_ind + 1:word_f_ind + 3]
#                 res.append((word_f, word_s))
#
#     return res


def delete_refs(line):
    """
    Удаляет референсы из статьи (если я ее пизжу с википедии)
    :param line: линия файла (т.е параграф)
    :return: ту же самую линию, но без рефов
    """

    res = ''

    line = line.split('[')
    for elem in line:
        if ']' in elem:
            n = 0
            while elem[n] != ']':
                n += 1
            res += elem[n + 1:]
        else:
            res += elem
    return res


def del_all_refs(path):
    """
    Удаляет все рефы в файле
    """

    text = ''
    with open(path, encoding='utf8') as f:
        for line in f:
            if line:
                line = delete_refs(line)
                text += line

    with open(path, 'w', encoding='utf8', newline='') as f:
        print(text, file=f)


del_all_refs('files_for_usolcev/1.txt')
