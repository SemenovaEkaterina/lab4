import random
from random import shuffle

MAX_CAP = 10**5
POPULATION_SIZE = 30
SELECTION_SIZE = 5
START = 0
END = 7


f = open('input2')
data = f.read()
data = data.split(';')
net_size = int(data[0])
PATH_SIZE = net_size
capacities = [None] * net_size
for value in range(net_size):
    capacities[value] = [0] * net_size
    capacities[value][value] = MAX_CAP

for value in data[1:]:
    line = value.split(',')
    from_x, to_x, result = int(line[0]), int(line[1]), int(line[2])
    capacities[from_x][to_x] = result
    capacities[to_x][from_x] = result

print(capacities)


def get_path_cap(path, values):
    min_value = MAX_CAP
    for i in range(len(path[1:])):
        length = values[path[i]][path[i+1]]
        min_value = length if length < min_value else min_value
        if path[i+1] == END and 0 < min_value < MAX_CAP:
            break
    return min_value


def cross(first_path, second_path):
    result_path = [None]*PATH_SIZE
    for j in range(PATH_SIZE):
        sample = random.randrange(0, 1)
        result_path[j] = first_path[j] if sample else second_path[j]

    return result_path


def make_mutation(path):
    first = random.randint(1, net_size-2)
    second = random.randint(1, net_size-2)
    path[first], path[second] = path[second], path[first]
    return path


def create_start_caps():
    paths = list()
    for i in range(POPULATION_SIZE):
        path = [x for x in range(net_size)]
        shuffle(path)
        paths.append(set_bounds(path, START, END))
    return paths


def set_bounds(path, start, end):
    path[0] = start
    path[len(path)-1] = end
    return path


def selection(paths):
    return sorted(paths,
                  key=lambda item: get_path_cap(item, capacities),
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
            print('path:', path, get_path_cap(path, capacities))


data = create_start_caps()
for value in range(100):
    data = new_generation(selection(data))

print_paths(data)
