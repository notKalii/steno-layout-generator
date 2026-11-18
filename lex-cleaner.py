import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('lexicon')

    args = parser.parse_args()

    lexicon = []
    with open(args.lexicon, 'r') as f:
        for line in f.readlines():
            lexicon.append(line.strip().split(':'))

    rev_lexicon = []
    lexicon_n = []
    conflicts = 0
    for entry in lexicon:
        if not entry[1] in rev_lexicon:
            lexicon_n.append(':'.join(entry))
            rev_lexicon.append(entry[1])
        else:
            conflicts += 1

    print(conflicts)

    with open('lexicon.txt', 'w') as f:
        for entry in lexicon_n:
            f.write(entry+'\n')