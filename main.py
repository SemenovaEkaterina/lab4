import random
from random import shuffle
import sys

MAX_CAP = 10**5
POPULATION_SIZE = 36
SELECTION_SIZE = 6

SELECTION_COUNT = int(sys.argv[1]) if len(sys.argv) > 1 else None

f = open('input')
data = f.read()
data = data.split(';')
NET_SIZE = int(data[0])
START = int(data[1])
END = int(data[2])
PATH_SIZE = NET_SIZE
capacities = [None] * NET_SIZE
for value in range(NET_SIZE):
    capacities[value] = [0] * NET_SIZE
    capacities[value][value] = MAX_CAP

for value in data[3:]:
    line = value.split(',')
    from_x, to_x, result = int(line[0]), int(line[1]), int(line[2])
    capacities[from_x][to_x] = result
    capacities[to_x][from_x] = result


def get_path_cap(path, values):
    min_value = MAX_CAP
    a = 0
    for i in range(len(path[1:])):
        length = values[path[i]][path[i+1]]
        min_value = length if length < min_value else min_value
        if path[i+1] == END and 0 < min_value < MAX_CAP:
            break
        if 0 < length < MAX_CAP:
            a += 1
    return min_value, a


def cross(first_path, second_path):
    result_path = [None]*PATH_SIZE
    for j in range(PATH_SIZE):
        sample = random.randrange(0, 1)
        result_path[j] = first_path[j] if sample else second_path[j]

    return result_path


def make_mutation(path):
    first = random.randint(1, NET_SIZE - 2)
    second = random.randint(1, NET_SIZE - 2)
    path[first], path[second] = path[second], path[first]
    return path


def create_start_caps():
    paths = list()
    for i in range(POPULATION_SIZE):
        path = [x for x in range(NET_SIZE)]
        shuffle(path)
        paths.append(set_bounds(path, START, END))
    return paths


def set_bounds(path, start, end):
    path[0] = start
    path[len(path)-1] = end
    return path


def selection(paths):
    return sorted(paths,
                  key=lambda item: get_path_cap(item, capacities)[0] + get_path_cap(item, capacities)[1],
                  reverse=True)[0:SELECTION_SIZE]


def new_generation(paths):
    size = len(paths)
    new_paths = []
    for i in range(size):
        for j in range(size):
            if i != j:
                new_paths.append(make_mutation(cross(paths[i], paths[j])))
    return new_paths + paths


def print_paths(paths):
    for path in paths:
        if path[0] == START and path[len(path)-1] == END:
            print(path,
                  get_path_cap(path, capacities)[0]+get_path_cap(path, capacities)[1],
                  get_path_cap(path, capacities)[0])


data = create_start_caps()


if SELECTION_COUNT:
    for value in range(SELECTION_COUNT):
        data = new_generation(selection(data))
    print_paths(selection(data))
else:
    while True:
        print_paths(selection(data))
        print('New generation?(y/n)')
        if input() != 'y':
            break
        data = new_generation(selection(data))
