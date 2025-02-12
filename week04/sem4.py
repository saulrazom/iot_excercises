#import random
from random import uniform


def random_net(n):
    return [[int(uniform(1, 2 * n)) for _ in range(n)] for _ in range(n)]


net1 = [[0, 4, 2, 1], [3, 0, 6, 5], [2, 3, 0, 2], [3, 8, 2, 0]]   # min_distance = 9
net2 = [[0, 4, 2, 1, 3, 5, 5, 6, 8, 6], [3, 0, 6, 5, 7, 2, 2, 5, 8, 2], [2, 3, 0, 2, 1, 4, 6, 8, 5, 4],
        [3, 8, 2, 0, 4, 5, 7, 9, 6, 5], [6, 1, 3, 8, 4, 2, 4, 7, 9, 1], [1, 2, 3, 4, 5, 6, 5, 9, 7, 8],
        [1, 2, 3, 4, 5, 6, 7, 4, 8, 3], [6, 5, 4, 3, 2, 1, 7, 8, 5, 3], [6, 3, 8, 7, 9, 1, 2, 5, 4, 5],
        [7, 3, 8, 9, 1, 2, 6, 5, 4, 6]]  # min_distance = 19
net3 = random_net(11)  # min_distance = ??
net  = net1


def process(st, k, visited, solution, d):
    return 0


def tsp_exhaustive(st):
    return 0


def get_nearest(st, visited):
    return 0


def tsp_nearest_neighbor(start):
    return 0


def eval(start, solution):
    return 0


def tsp_random(start, n):
    return 0


if __name__ == '__main__':
    minD = tsp_random(0, 10000)
    print(minD)
    minD = tsp_exhaustive(0)
    print(minD)
    minD = tsp_nearest_neighbor(0)
    print(minD)
