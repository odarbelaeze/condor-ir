def normalize(word):
    return word.lower()


def words():
    # las saca de un archivo o de una base de datos por ejemplo
    with open('words', 'r') as f:
        for line in f:
            yield line


def normalized(wordseq):
    return map(normalize, wordseq)


if __name__ == '__main__':
    print(normalized(words()))
    for word in sorted(normalized(words())):
        print(word)
