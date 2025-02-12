from random import uniform
from math import cos, pi, exp, sqrt,  e
from time import time


def randx(xl, xh, dim):
  return [uniform(xl[i], xh[i]) for i in range(dim)]
  

def random_min(func, xl, xh, dim, n):
  xm = ()
  fm = float('inf')
  for i in range(n):
      x = randx(xl, xh, dim)
      f = func(x, dim)
      if f < fm:
          fm = f
          xm = x
  return xm


def hc_min(func, xl, xh, dim, n):
  xbest = randx(xl, xh, dim)
  ybest = func(xbest, dim)
  DX = [xh[i] - xl[i] for i in range(dim)]
  dx = [-DX[i] / 2 + uniform(0, DX[i]) for i in range(dim)]
  x = [0 for _ in range(dim)]
  for i in range(n):
      for i in range(dim): x[i] = xbest[i] + dx[i]
      y = func(x, dim)
      if y < ybest:
          ybest = y
          for i in range(dim): xbest[i] = x[i]
          fit = 1 / (1 + ybest)
          for i in range(dim): DX[i] = (xh[i] - xl[i]) * (1 - fit)
      else:
          for i in range(dim): dx[i] = -DX[i] / 2 + uniform(0, DX[i])
  return xbest


def pso_min(func, xlow, xhigh, dim, n):
    w = 0.001
    c1 = 0.1
    c2 = 0.1
    m = 1000

    # xlow y xhigh deben ser igual que dim
    if len(xlow) != dim or len(xhigh) != dim:
        xlow = [xlow[0]] * dim
        xhigh = [xhigh[0]] * dim

    # Inicializar lista de M partículas con (posición aleatoria, velocidad aleatoria, la misma posición aleatoria)
    particles = []
    global_best_pos = None
    global_best_val = float('inf')

    for _ in range(m):
        position = [uniform(xlow[i], xhigh[i]) for i in range(dim)]
        velocity = [uniform(-0.5, 0.5) for _ in range(dim)]
        local_best_pos = position[:]
        # Mientras se inicializa, registrar índice de la mejor posición, ello implica utilizar la función a minimizar
        local_best_val = func(position, dim)  

        if local_best_val < global_best_val:
            global_best_pos = local_best_pos[:]
            global_best_val = local_best_val

        particles.append((position, velocity, local_best_pos, local_best_val))

    # Por cada generación de 1 a n
    for _ in range(n):
        # Por cada partícula p de 1 a m
        for i in range(m):
            position, velocity, local_best_pos, local_best_val = particles[i]

            r1, r2 = uniform(0, 1), uniform(0, 1)
            # Actualizar la velocidad de p  
            new_velocity = []
            for d in range(dim):
                new_velocity.append( w * velocity[d] + c1 * r1 * (local_best_pos[d] - position[d]) + c2 * r2 * (global_best_pos[d] - position[d]))

            #  Actualizar posición de p en términos de la velocidad
            new_position = [position[d] + new_velocity[d] for d in range(dim)]
            new_val = func(new_position, dim)  

            # Actualizar su mejor posición local, en términos de la función a minimizar
            if new_val < local_best_val:
                local_best_pos = new_position[:]
                local_best_val = new_val

            # Si es el caso, actualizar la mejor posición global
            if new_val < global_best_val:
                global_best_pos = new_position[:]
                global_best_val = new_val

            particles[i] = (new_position, new_velocity, local_best_pos, local_best_val)

    # devolver la posición x de la mejor partícula
    return global_best_pos, global_best_val


# Funciones de prueba
def rosenbrock(x, dim):
    fx = 0
    for i in range(dim - 1):
        fx += 100 * (x[i + 1] - x[i] ** 2) ** 2 + (1 - x[i]) ** 2
    return fx


def rastrigin(x, dim):
    fx = 0
    for i in range(dim):
        fx += x[i] ** 2 - 10 * cos(2 * pi * x[i])  
    return 10 * dim + fx


def styblinski(x, dim):
    fx = 0
    for i in range(dim):
        fx += x[i] ** 4 - 16 * x[i] ** 2 + 5 * x[i]
    return fx / 2

def ackley(x, dim):
    sum1 = 0
    sum2 = 0
    
    for i in range(dim):
        sum1 += x[i] ** 2
        sum2 += cos(2 * pi * x[i])
    
    term1 = -20 * exp(-0.2 * sqrt(sum1 / dim))
    term2 = -exp(sum2 / dim)
    
    return term1 + term2 + 20 + e


if __name__ == '__main__':
    functions = {
        "Rosenbrock": rosenbrock,
        "Rastrigin": rastrigin,
        "Styblinsky-Tang": styblinski,
        "Ackley": ackley

    }

    n = 1000
    dim = 5
    xlow = [-5 for _ in range(dim)]
    xhigh = [5 for _ in range(dim)]

    for name, func in functions.items():
        print(f"\n{name}:")
        start = time()
        minx = pso_min(func, xlow, xhigh, dim, n)
        end = time()
        print(f"x={minx}")
        print(f"f(x)={func(minx[0], dim):.9f}") 
        print(f"{(end - start):.2f} seconds")
