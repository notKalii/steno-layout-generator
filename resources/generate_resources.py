import argparse
import json

def syllable_freq(lexicon):
    freq = {}
    for line in lexicon:
        word = line[1].split('/')
        for syl in word:
            if syl in freq:
                freq[syl] += 1
            else:
                freq[syl] = 1
    return freq

def parse(filename):
    lexicon = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            lexicon.append(line.strip().split(':'))

    return lexicon

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')

    args = parser.parse_args()
    lexicon = parse(args.filename)

    freq = syllable_freq(lexicon)
    with open('resources/resources.json', 'w') as f:
        json.dump(freq, f, indent=2)