#import random
from random import uniform, shuffle, seed
from time import time


def random_net(n):
    return [[int(uniform(1, 2 * n)) for _ in range(n)] for _ in range(n)]


net1 = [[0, 4, 2, 1], [3, 0, 6, 5], [2, 3, 0, 2], [3, 8, 2, 0]]   # min_distance = 9
net2 = [[0, 4, 2, 1, 3, 5, 5, 6, 8, 6], [3, 0, 6, 5, 7, 2, 2, 5, 8, 2], [2, 3, 0, 2, 1, 4, 6, 8, 5, 4],
        [3, 8, 2, 0, 4, 5, 7, 9, 6, 5], [6, 1, 3, 8, 4, 2, 4, 7, 9, 1], [1, 2, 3, 4, 5, 6, 5, 9, 7, 8],
        [1, 2, 3, 4, 5, 6, 7, 4, 8, 3], [6, 5, 4, 3, 2, 1, 7, 8, 5, 3], [6, 3, 8, 7, 9, 1, 2, 5, 4, 5],
        [7, 3, 8, 9, 1, 2, 6, 5, 4, 6]]  # min_distance = 19
net3 = random_net(11)  # min_distance = ??
net  = net2

#### Algoritmo exhaustivo
def process(st, k, visited, solution, d, nt):
    # Si k = n, ya tenemos la permutación completa y podemos devolver la distancia total
    n = len(nt)
    if k == n:
        return d + nt[solution[k - 1]][st]
    #Si no, tenemos que intentar todas las posibilidades para la posición k, y devolver la mínima distancia de todas.
    minD = float('inf')
    for i in range(n):
        if not visited[i]:
            visited[i] = True
            solution[k] = i
            # d = process(st, k+1, ...)
            # minD = min(minD, d)
            minD = min(minD, process(st, k + 1, visited, solution, d + nt[solution[k - 1]][solution[k]], nt))
            visited[i] = False
    return minD
   
def tsp_exhaustive(st, nt):
    n = len(nt)
    # Si st = 2, n = 6
    # ¿ Cómo generamos estas listas por "Comprensión"?
    # visited = [ False, False, True, False, False, False] --> Tamaño N
    # solution = [2, -1, -1, -1, -1, 2] --> Tamaño N + 1
    # Llamar a process pasando estos datos con k = 1, d = 0
    visited = [False if i != st else True for i in range(n)]
    solution = [st if i == 0 or i == n else -1 for i in range(n + 1)]
    return process(st, 1, visited, solution, 0, nt)
    

#### Algoritmo vecino más cercano
def get_nearest(st, visited):
    return 0


def tsp_nearest_neighbor(start):
    return 0


#### Algoritmo aleatorio
def eval(start, solution, nt):
    #calcular la distancia de la solución/secuencia utilizando G
    d = 0
    n = len(nt)
    for i in range(n - 1):
        d += nt[solution[i]][solution[i + 1]]
    d += nt[solution[-1]][start]
    return d
   
def tsp_random(start, m, nt): # m = iterations
    n = len(nt)
    # Solución inicial [0, 1, 2.., N – 2] reemplazando S por N – 1
    solution = [i for i in range(n) if i != start]
    solution.append(start)

    #Evaluar la solución
    minD = eval(start, solution, nt)

    # Repetir m veces
    for _ in range(m):
        # Revolver la secuencia anterior (shuffle)
        shuffle(solution[:-1])
        # Calcular la distancia de la nueva secuencia aleatoria
        d = eval(start, solution, nt)
        # Actualizar la distancia mínima, si aplica
        if d < minD:
            minD = d

    return minD

if __name__ == '__main__':
    start = time()
    minD = tsp_random(0, 100000, net)
    end = time()
    print(f"\nTSP RANDOM\nMin distance: {minD}\n{(end - start):.2f} seconds")

    start = time()
    minD = tsp_exhaustive(2, net)
    end = time()
    print(f"\nTSP EXHAUSTIVE\nMin distance: {minD}\n{(end - start):.2f} seconds")

    start = time()
    minD = tsp_nearest_neighbor(0)
    end = time()
    print(f"\nTSP NEAREST NEIGHBOR\nMin distance: {minD}\n{(end - start):.2f} seconds")
