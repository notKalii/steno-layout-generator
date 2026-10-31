import argparse
import json
import pickle

class Resources:
    def __init__(self, syllables, frequency, phonemes, strokes):
        self.syllables = syllables
        self.frequency = frequency
        self.onsets = phonemes[0]
        self.nuclei = phonemes[1]
        self.codas = phonemes[2]
        self.strokes = strokes

    def valid(self, stroke):
        s = format(stroke, '016b')
        if s[2:6] in ['0110', '0111', '1001', '1011', '1101', '1110']: return False
        if s[9:12] in ['0110', '0111', '1001', '1011', '1101', '1110']: return False
        if s[9] in ['101', '111']: return False
        if s[12:] in ['101', '111']: return False
    
        return True

def syllable_freq(lexicon):
    freq = {}
    syls = []
    for line in lexicon:
        word = line[1].split('/')
        for syl in word:
            if syl in freq:
                freq[syl] += 1
            else:
                syls.append(syl)
                freq[syl] = 1
    return (syls, freq)

def strokes():
    f0 = ['00', '01', '10', '11']
    f1 = ['0000', '0001', '0010', '0100', '1000', '0011', '1100', '1010', '0101', '1111']
    f2 = ['000', '001', '010', '100', '011', '110', '111']
    stroke_list = []

    for a in range(len(f0)):
        for b in range(len(f1)):
            for c in range(len(f2)):
                for d in range(len(f2)):
                    for e in range(len(f1)):
                        stroke = f0[a]+f1[b]+f2[c]+f2[d]+f1[e]
                        stroke_list.append(int(stroke, 2))

    return stroke_list

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

    syl_freq = syllable_freq(lexicon)
    phonemes = phoneme_list(lexicon)
    stroke_list = strokes()
    resources = Resources(syl_freq[0], syl_freq[1], phonemes, stroke_list)

    with open('resources.pickle', 'wb') as f:
        pickle.dump(resources, f)