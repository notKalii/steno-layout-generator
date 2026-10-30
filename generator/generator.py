import argparse
import json
import random

POPULATION_SIZE = 1000

class Layout:
    def __init__(self):
        self.o = {}
        self.n = {}
        self.c = {}

def valid(stroke):
    s = format(stroke, '016b')
    if s[2:6] in ['0110', '0111', '1001', '1011', '1101', '1110']: return False
    if s[9:12] in ['0110', '0111', '1001', '1011', '1101', '1110']: return False
    if s[9] in ['101', '111']: return False
    if s[12:] in ['101', '111']: return False

    return True

def random_layout(phonemes, strokes):
    layout = Layout()
    for onset in phonemes[0]: layout.o[onset] = strokes[random.randint(0, len(strokes)-1)]
    for nucleus in phonemes[1]: layout.n[nucleus] = strokes[random.randint(0, len(strokes)-1)]
    for coda in phonemes[2]: layout.c[coda] = strokes[random.randint(0, len(strokes)-1)]

    return layout

def generate(lexicon, syllables, phonemes, strokes):
    # Initialise population
    population = []
    for i in range(POPULATION_SIZE): population.append(random_layout(phonemes, strokes))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('path')
    parser.add_argument('lexicon')
    parser.add_argument('syllables')
    parser.add_argument('phonemes')
    parser.add_argument('strokes')

    args = parser.parse_args()
    lexicon = []
    with open(args.path+args.lexicon, 'r') as f:
        for line in f.readlines():
            lexicon.append(line.strip().split(':'))
    with open(args.path+args.syllables, 'r') as f:
        syllable_freq = json.load(f)
    phonemes = []
    with open(args.path+args.phonemes, 'r') as f:
        for line in f.readlines():
            phonemes.append(line.strip())
    strokes = []
    with open(args.path+args.strokes, 'r') as f:
        for line in f.readlines():
            strokes.append(int(line.strip()))

    generate(lexicon, syllable_freq, phonemes, strokes)