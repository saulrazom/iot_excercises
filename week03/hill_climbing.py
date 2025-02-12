from random import uniform, random
from math import cos, pi

def randx(xlow, xhigh):
  return uniform(xlow[0], xhigh[0]), uniform(xlow[1], xhigh[1])

def max_DX(xlow, xhigh, fitness):
    return ((xhigh[0] - xlow[0])*(1-fitness), (xhigh[1] - xlow[1])*(1-fitness))

def increment(Dx):
    return (-0.5*Dx[0]+random()*Dx[0], -0.5*Dx[1]+random()*Dx[1])

def hill_climbing(func, xlow, xhigh, n):
      # 1. Crear una solución aleatoria en la zona factible [x0, x1]
    x = (uniform(xlow[0], xhigh[0]), uniform(xlow[1], xhigh[1]))
     # 2. Calcula y = funcion(x)
    y = func(x)
     # 3. Calcular el incremento máximo DX
    Dx = max_DX(xlow, xhigh, 0)
     # 4. Calcular el incremento aleatorio dx delimitado por DX
    dx = increment(Dx)

      # 5. Por cada iteración:
    for _ in range(n):
        # a. Crear una solución x = mejor_solucion + incremento
        x1 = (x[0] + dx[0], x[1] + dx[1])
        # b. Calcular y = función(x)
        curr = func(x1)
         #  c. Si y es mejor que el actual mejor:
        if(curr < y):
            # i.  Actualizar x, y mejores
            x, y = x1, curr
            # ii. Hacer más fino el máximo incremento DX en términos de la aptitud
            Dx = max_DX(xlow, xhigh, 1/(1+y))
        #  d. Si no:
        else:
            # i. Calcular nuevo incremento aleatorio dx
            dx = increment(Dx)
    # 6. Devolver mejor x
    return (x, y)

  
def random_min(func, xlow, xhigh, n):
  xm = ()
  fm = float('inf')
  for i in range(n):
    x = randx(xlow, xhigh)
    f = func(x)
    if f < fm:
      fm = f
      xm = x
  return xm


# 𝑓(𝑥) = 100(𝑥2 − 𝑥1^2)^2 + (1 − 𝑥1)^2
def rosenbrock(x):
  return 100 * (x[1] - x[0]**2)** 2 + (1 - x[0])**2


def rastrigin(x):
  return 20 + x[0] ** 2 - 10 * cos(2 * pi * x[0]) + x[1] ** 2 - 10 * cos(2 * pi * x[1])


def styblinski(x):
  return (x[0] ** 4 - 16 * x[0] ** 2 + 5 * x[0] + x[1] ** 4 - 16 * x[1] ** 2 + 5 * x[1]) / 2


if __name__ == '__main__':
  functions = {
        "Rosenbrock": rosenbrock,
        "Rastrigin": rastrigin,
        "Styblinsky-Tang": styblinski,
  }
     
  xlow = (-5, -5)
  xhigh = (5, 5)
  n = 10000

  # print("===== Random_Min =====")
  # for name, func in functions.items():
  #   print(f"\n{name}")
  #   xmin = random_min(func, xlow, xhigh, 10000000)
  #   print("xmin =", xmin)
  #   f = func(xmin)
  #   print(f"f(xmin) = {f:.8f}")

  print(f"\n===== Hill Climbing n = {n} =====")
  for name, func in functions.items():
    print(f"\n{name}")
    res = hill_climbing(func, xlow, xhigh, n)
    print("xmin =", res[0])
    print(f"f(xmin) = {res[1]:.8f}")





  
  

 