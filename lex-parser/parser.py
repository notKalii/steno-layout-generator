import argparse

def parse_pron(pron):
    pass
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

    return output

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')

    args = parser.parse_args()
    parse(args.filename)