from random import shuffle


def create_anagrams(line):
    symbols = list(line)
    shuffle(symbols)
    return ' '.join(symbols)


print('Через пробел введите слова')
words = input().split()
for word in words:
    print(create_anagrams(word))