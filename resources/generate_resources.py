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

def phoneme_list(lexicon):
    onsets = []
    nuclei = []
    codas = []

    for line in lexicon:
        word = line[1].split('/')
        for syl in word:
            s = syl.split(' ')
            for char in s[0]:
                if not char in onsets:
                    onsets.append(char)
            for char in s[1]:
                if not char in nuclei:
                    nuclei.append(char)
            for char in s[2]:
                if not char in codas:
                    codas.append(char)

    return [onsets, nuclei, codas]

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

    phonemes = phoneme_list(lexicon)
    with open('resources/phonemes.txt', 'w') as f:
        for p in phonemes[0]:
            f.write(p)
        f.write('\n')
        for p in phonemes[1]:
            f.write(p)
        f.write('\n')
        for p in phonemes[2]:
            f.write(p)