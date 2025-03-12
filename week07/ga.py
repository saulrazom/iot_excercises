from random import randrange, random, randint
import copy

class Individual:
    def __init__(self, genotype, phenotype, fitness, expectedValue):
        self.genotype = genotype
        self.phenotype = phenotype
        self.fitness = fitness
        self.expectedValue = expectedValue

    def __repr__(self):
        return f'Genotype: {self.genotype}, Phenotype: {self.phenotype}, Fitness: {self.fitness}, Expected Value: {self.expectedValue}'


def styblinski(x, dim=2):
    fx = 0
    for i in range(dim):
        fx += pow(x[i], 4) - 16 * pow(x[i], 2) + 5 * x[i]
    return fx / 2


def fitness(x, fxl, fxh):
    if fxh == fxl:
        return 1.0  # Avoid division by zero
    return 1 - (styblinski(x) - fxl) / (fxh - fxl)


def updateFitness(pop, fxl, fxh):
    best = copy.deepcopy(pop[0])
    for ind in pop:
        ind.fitness = fitness(ind.phenotype, fxl, fxh)
        if ind.fitness > best.fitness:
            best = copy.deepcopy(ind)
    return best


def toPhenotype(genotype, xl, xh):
    x1 = 0
    f = 1
    l = len(genotype) - 1
    m = l // 2
    max_val = 0
    for i in range(m, -1, -1):
        x1 += genotype[i] * f
        max_val += 9 * f
        f *= 10
    if max_val == 0:
        x1 = xl[0]
    else:
        x1 = xl[0] + x1 / max_val * (xh[0] - xl[0])
    
    x2 = 0
    f = 1
    for i in range(l, m, -1):
        x2 += genotype[i] * f
        f *= 10
    if max_val == 0:
        x2 = xl[0]
    else:
        x2 = xl[0] + x2 / max_val * (xh[0] - xl[0])
    return x1, x2


def createPop(M, xl, xh):
    pop = []
    for _ in range(M):
        genotype = [randrange(0, 10) for _ in range(12)]
        phenotype = toPhenotype(genotype, xl, xh)
        pop.append(Individual(genotype, phenotype, 0, 0))
    return pop


def selection(pop):
    # Ordernar la población por fitness de menor a mayor
    pop = sorted(pop, key=lambda x: x.fitness)
    n = len(pop)

    # Iterar la ponblación ordenada y calcular el valor esperado, utilizando la posición de cada individuo como jerarquía
    for i in range(n):
        pop[i].expectedValue = 0.9 + (1.1 - 0.9) * i / (n -1)

    # Crear nueva población e insertar un clon del mejor de la generación pasada.
    new_pop = [copy.deepcopy(pop[0])]

    # Girar ruleta N-1 veces
    for _ in range(n - 1):
        # Generar un aleatorio entre 0 y el tamaño de la población.
        r = randrange(0, n) 
        # Calcular la sumatoria de los valores esperados de los individuos
        sum = 0
        i = 0
        # Añadir  a la nueva población al clon del individuo al momento en que la sumatoria superó al número aleatorio.
        while sum < r:
            sum += pop[i].expectedValue
            i += 1

        # Devolver la nueva población
    return new_pop
       
def crossover(pop):
    n = len(pop)
    # La cruza será Uniforme de 2 puntos. Probabilidad: 0.8
    # Ejecutar lo siguiente por cada par de individuos adyacentes, excepto el mejor individuo y su vecino (elitista):
    for i in range(1, n - 1, 2):
         # 1. Si un aleatorio en el rango [0..1] es mayor que 0.8, continuar con el siguiente par
        if random() > 0.8:
            continue    
        # 2. Obtener dos índices aleatorios 𝑖1, 𝑖2, tal que 𝑖1< 𝑖2:
        i1 = randrange(0, 12)
        i2 = randrange(i1, 12)

        # 3. Desde 𝑖 = 𝑖1 hasta 𝑖2: Si un aleatorio en el rango [0..1] es menor que 0.5, intercambiar los alelos en la posición 𝑖 de los dos individuos.
        for j in range(i1, i2):
            if random() < 0.5:
                pop[i].genotype[j], pop[i + 1].genotype[j] = pop[i + 1].genotype[j], pop[i].genotype[j]
        
    return pop


def mutation(pop):
    # La mutación será Uniforme. Probabilidad: 0.2

    # Ejecutar lo siguiente por cada individuo, excepto con el mejor (elitista):
    for i in range(1, len(pop)):  # Comenzar desde 1 para omitir al mejor individuo
        # 1. Si un aleatorio en el rango [0..1] es mayor que 0.2, continuar con el siguiente
        if random() > 0.2:  # Verificar probabilidad de mutación
            continue

        # 2. Seleccionar una posición aleatoria del genotipo.
        pos = randint(0, len(pop[i].genotype) - 1)  # Índice aleatorio en el genotipo

        # 3. Calcular un nuevo valor aleatorio en el rango permitido [0..9].
        pop[i].genotype[pos] = randint(0, 9)  # Asignar un nuevo valor aleatorio


def runGA(N, M, xl, xh, fxl, fxh):
    pop = createPop(M, xl, xh)  # Create population
    bf = 0  # Best fitness
    for i in range(N):
        best = updateFitness(pop, fxl, fxh)
        if bf < best.fitness:
            bf = best.fitness
            print(f'i={i:2d}, fitness={bf:.8f}')
        selection(pop)
        crossover(pop)
        mutation(pop)
    best = updateFitness(pop, fxl, fxh)
    return best.phenotype


if __name__ == '__main__':
    min = runGA(1000, 100, [-5, -5], [5, 5], -80, 250)  # Generaciones, tamaño de población, mínimos, máximos y mínimo de fx y máximo de fx.
    print(min, styblinski(min))

    # x=[−2.903535,−2.903534]
    # f(x)=−78.3323314