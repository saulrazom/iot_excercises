#import random
from random import uniform, shuffle, seed, choice
from time import time
from math import exp


def random_net(n):
    return [[int(uniform(1, 2 * n)) for _ in range(n)] for _ in range(n)]


net1 = [[0, 4, 2, 1], [3, 0, 6, 5], [2, 3, 0, 2], [3, 8, 2, 0]]   # min_distance = 9
net2 = [[0, 4, 2, 1, 3, 5, 5, 6, 8, 6], [3, 0, 6, 5, 7, 2, 2, 5, 8, 2], [2, 3, 0, 2, 1, 4, 6, 8, 5, 4],
        [3, 8, 2, 0, 4, 5, 7, 9, 6, 5], [6, 1, 3, 8, 4, 2, 4, 7, 9, 1], [1, 2, 3, 4, 5, 6, 5, 9, 7, 8],
        [1, 2, 3, 4, 5, 6, 7, 4, 8, 3], [6, 5, 4, 3, 2, 1, 7, 8, 5, 3], [6, 3, 8, 7, 9, 1, 2, 5, 4, 5],
        [7, 3, 8, 9, 1, 2, 6, 5, 4, 6]]  # min_distance = 19
net3 = random_net(11)  # min_distance = ??

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
    

def get_nearest(st, visited, nt):
    n = len(nt)
    nearest = -1
    minD = float('inf')
    for i in range(n):
        if not visited[i] and nt[st][i] < minD:
            minD = nt[st][i]
            nearest = i
    return nearest

### Algoritmo de vecino más cercano
def tsp_nearest_neighbor(start, nt):  # El método recibe el índice del nodo inicial/final S y el grafo G.
    n = len(nt)
    # Sea C(urrent) <- S(tart)
    curr = start
    # Añadir S a los visitados
    visited = [False for _ in range(n)]
    visited[start] = True
    minD = 0
    # Repetir N – 1 veces:
    for _ in range(n - 1):
        # Sea N(earest) el índice del nodo no visitado más cercano a C, utilizando G
        nearest = get_nearest(curr, visited, nt)
        # Añadir N a los visitados
        visited[nearest] = True
        # Sumar a la distancia total la distancia de C a N
        minD += nt[curr][nearest]
        # C <- N
        curr = nearest
    # Sumar a la distancia total la distancia de N a S
    minD += nt[curr][start]
    # Devolver la distancia total
    return minD


#### Algoritmo aleatorio
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

def eval(start, solution, nt):
    d = 0
    n = len(solution)
    d += nt[start][solution[0]]
    for i in range(n - 1):
        d += nt[solution[i]][solution[i + 1]]
    d += nt[solution[-1]][start]
    return d

#### Reconocido Simulado
def swap(solution):
    n = len(solution)
    i = int(uniform(0, n))
    j = int(uniform(0, n))
    while i == j:  
        j = int(uniform(0, n))
    solution[i], solution[j] = solution[j], solution[i]
    return solution

def inverse(solution):
    n = len(solution)
    i = int(uniform(0, n))
    j = int(uniform(0, n))
    if i > j:
        i, j = j, i
    solution[i:j] = solution[i:j][::-1]
    return solution

def insert(solution):
    n = len(solution)
    i = int(uniform(0, n))
    j = int(uniform(0, n))
    while i == j: 
        j = int(uniform(0, n))
    solution.insert(j, solution.pop(i))
    return solution
    
def move_to_neighbor(solution):
    perturbation = choice([swap, inverse, insert])
    return perturbation(solution)

# Función fitness (energía)
def f(start, solution, nt):
    return 1 / eval(start, solution, nt)

def tsp_sa(start, n, nt):
    T = 100  
    alpha = 0.99 
    d = 100000
    
    # x1 = permutación aleatoria sin incluir a start
    x1 = [i for i in range(len(nt)) if i != start]
    
    for _ in range(n):
        # x2 = un nuevo vecino de x1
        x2 = move_to_neighbor(x1.copy())
        
        # calcular fx1, fx2
        fx1 = f(start, x1, nt)
        fx2 = f(start, x2, nt)
        
        # si x2 mejoró/empató a x1, reemplazarlo
        if fx2 >= fx1:
            x1 = x2
        # si no, utilizar la distribución de probabilidad de Boltzmann
        else:
            if uniform(0, 1) < exp((fx2 - fx1) / T):
                x1 = x2
        
        # actualizar d 
        current_distance = eval(start, x1, nt)
        if current_distance < d:
            d = current_distance
        
        T *= alpha
    
    return d



if __name__ == '__main__':
    test_net = net3
    for row in test_net:
        print("  ".join(f"{num:2d}" for num in row))
    start = time()
    minD = tsp_random(0, 100000, test_net)
    end = time()
    print(f"\nTSP RANDOM\nMin distance: {minD}\n{(end - start):.2f} seconds")

    start = time()
    minD = tsp_exhaustive(2, test_net)
    end = time()
    print(f"\nTSP EXHAUSTIVE\nMin distance: {minD}\n{(end - start):.2f} seconds")

    start = time()
    minD = tsp_nearest_neighbor(0, test_net)
    end = time()
    print(f"\nTSP NEAREST NEIGHBOR\nMin distance: {minD}\n{(end - start):.2f} seconds")

    start = time()
    minD = tsp_sa(0, 100000, test_net)
    end = time()
    print(f"\nTSP SA\nMin distance: {minD}\n{(end - start):.2f} seconds")
