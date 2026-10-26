import argparse

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
trans_table = {}


def parse_pron(pron):
    token = ''
    vowel_ = False
    section = ''
    syllable = []
    word = []
    for char in pron+'.':
        if char in ['{', '}', '<', '>', '*', '$', '=', '-', '~']:
            continue

        if char == ' ':
            if token != '':
                if token[-1] == '!':
                    token = token[:-1]
                    syllable.append(section)
                    syllable.append('')
                    section = ''
                if (token[0] in 'aeiou@') != vowel_:
                    syllable.append(section)
                    section = ''
                    vowel_ = not vowel_
                if len(token) > 1:
                    if token in trans_table:
                        token = trans_table[token]
                    else:
                        trans_table[token] = token = ALPHABET[len(trans_table.keys())]
                section += token
                token = ''
            continue

        if char == '.':
            section += token
            syllable.append(section)
            while len(syllable) < 3:
                syllable.append('')
            word.append(' '.join(syllable))
            syllable = []
            section = ''
            token = ''
            vowel_ = False
            continue

        token += char
    return '/'.join(word)

def parse_morph(morph):
    affix_open = False
    index = 0
    output = [[], '', []]
    token = ''
    for char in morph:
        if char in [' ', '-', '=']:
            continue

        if char == '{':
            index = 2
            continue

        if char == '}':
            output[1] += token
            token = ''
            continue

        if char in ['<', '>']:
            if affix_open:
                affix_open = False
                output[index].append(token)
                token = ''
            else:
                affix_open = True
            continue

        token += char

    output2 = [' '.join(output[0]), output[1], ' '.join(output[2])]

    return '/'.join(output2)

def parseline(line):
    # Identifier (anything greater than 1, or any non-blank string, is removed)
    if not (line[1] == '' or line[1][0] == '1'): return

    # Part of speech (proper nouns removed)
    remove = True
    for x in line[2].split('/'):
        if not any(y in ['NNP', 'NNPS'] for y in x.split('|')):
            remove = False
    if remove: return

    name = line[0]
    pron = parse_pron(line[3])
    morph = parse_morph(line[4])

    return [name, pron, morph]

def parse(filename):
    lexicon = []
    with open(filename) as f:
        for line in f.readlines():
            l = parseline(line.strip().split(':'))
            if l != None:
                lexicon.append(l)

    return lexicon

def save_file(lexicon, folder='lex-parser/', lexFile='parsed', transFile='trans_table'):
    with open(folder+lexFile+'.txt', 'w') as f:
        for line in lexicon:
            f.write(':'.join(line)+'\n')
    with open(folder+transFile+'.txt', 'w') as f:
        for token in trans_table.keys():
            f.write(token+' - '+trans_table[token]+'\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')

    args = parser.parse_args()
    lexicon = parse(args.filename)
    save_file(lexicon)