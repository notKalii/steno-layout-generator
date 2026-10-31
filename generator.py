import argparse
import pickle
import random
import threading
import timeit

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

def random_layout():
    layout = Layout()
    for onset in resources.onsets: layout.o[onset] = resources.strokes[random.randint(0, len(resources.strokes)-1)]
    for nucleus in resources.nuclei: layout.n[nucleus] = resources.strokes[random.randint(0, len(resources.strokes)-1)]
    for coda in resources.codas: layout.c[coda] = resources.strokes[random.randint(0, len(resources.strokes)-1)]

    return layout

def score_layout(start_point, interval):
    print(f'Thread {int(start_point/interval)+1} started')
    for i in range(start_point, start_point+interval):
        layout = population[i]
        conflicts_list = []
        conflicts = 0
        for syl in resources.syllables:
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

def generate():
    global population
    ts = timeit.default_timer()
    # Initialise population
    population = []
    for i in range(POPULATION_SIZE): population.append(random_layout())
    te = timeit.default_timer()
    print(f'Population intialised ({round(te-ts, 5)})')

    # Score layout
    ts = timeit.default_timer()
    threads = []
    start_point = 0
    interval = int(POPULATION_SIZE / THREAD_COUNT)
    for i in range(THREAD_COUNT): 
        threads.append(
            threading.Thread(target=score_layout, args=(start_point, interval))
        )
        print(f'Thread {i} created')
        start_point += interval
    clear_lines(8)
    for t in threads: t.start()
    clear_lines(8)
    for t in threads: t.join()
    clear_lines(8)
    te = timeit.default_timer()
    print(f'Scoring complete ({round(te-ts, 5)})')
    avgScore = 0
    for layout in population: avgScore += layout.score
    print(avgScore/POPULATION_SIZE)

if __name__ == '__main__':
    global resources
    global lexicon

    parser = argparse.ArgumentParser()

    parser.add_argument('lexicon')
    parser.add_argument('resources')

    args = parser.parse_args()

    lexicon = []
    with open(args.lexicon, 'r') as f:
        for line in f.readlines():
            lexicon.append(line.strip().split(':'))
    with open(args.resources, 'rb') as f:
        resources = pickle.load(f)

    generate()