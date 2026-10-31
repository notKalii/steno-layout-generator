import argparse
import json
import random
import threading

POPULATION_SIZE = 1000
THREAD_COUNT = 8

class Layout:
    def __init__(self):
        self.o = {}
        self.n = {}
        self.c = {}
        self.score = -1

def clear_lines(n=1):
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    for i in range(n):
        print(LINE_UP, end=LINE_CLEAR)

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

def score_layout(population, syllables, start_point, interval):
    print(f'Thread {int(start_point/interval)+1} started')
    for i in range(start_point, start_point+interval):
        layout = population[i]
        conflicts_list = []
        conflicts = 0
        for syl in syllables.keys():
            stroke = 0
            s = syl.split(' ')
            for char in s[0]: stroke = stroke | layout.o[char]
            for char in s[1]: stroke = stroke | layout.n[char]
            for char in s[2]: stroke = stroke | layout.c[char]
            if stroke in conflicts_list:
                conflicts += 1
            else:
                conflicts_list.append(stroke)
        population[i].score = conflicts
    print(f'Thread {int(start_point/interval)+1} finished')

def generate(lexicon, syllables, phonemes, strokes):
    # Initialise population
    population = []
    for i in range(POPULATION_SIZE): population.append(random_layout(phonemes, strokes))
    print('Population intialised')

    # Score layout
    threads = []
    start_point = 0
    interval = int(POPULATION_SIZE / THREAD_COUNT)
    for i in range(THREAD_COUNT): 
        threads.append(
            threading.Thread(target=score_layout, args=(population, syllables, start_point, interval))
        )
        print(f'Thread {i} created')
        start_point += interval
    clear_lines(8)
    for t in threads: t.start()
    clear_lines(8)
    for t in threads: t.join()
    clear_lines(8)
    avgScore = 0
    for layout in population: avgScore += layout.score
    print(avgScore/POPULATION_SIZE)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('lexicon')
    parser.add_argument('syllables')
    parser.add_argument('phonemes')
    parser.add_argument('strokes')

    args = parser.parse_args()
    lexicon = []
    with open(args.lexicon, 'r') as f:
        for line in f.readlines():
            lexicon.append(line.strip().split(':'))
    with open(args.syllables, 'r') as f:
        syllable_freq = json.load(f)
    phonemes = []
    with open(args.phonemes, 'r') as f:
        for line in f.readlines():
            phonemes.append(line.strip())
    strokes = []
    with open(args.strokes, 'r') as f:
        for line in f.readlines():
            strokes.append(int(line.strip()))

    generate(lexicon, syllable_freq, phonemes, strokes)