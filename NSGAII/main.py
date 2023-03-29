import math
from problems.zdt1 import ZDT1

from DynamicUtils import DynamicUtils
from Evolution import Evolution

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.problems import get_problem
from pymoo.util.plotting import plot
from pymoo.optimize import minimize

import matplotlib.pyplot as plt



n_individuals = 100 #100
n_generations = 10
n_variables = 30
min = 0
max = 1


zdt1 = ZDT1(n_variables)
dynamic_evolution = DynamicUtils(zdt1, n_individuals, n_generations)
algorithm = Evolution(zdt1, n_individuals, n_generations)

# Generation of the population and initialization
population = []
for i in range(n_individuals):
    population = dynamic_evolution.generate_random_solutions(min, max, n_variables)

print(population)

print(';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;')

#print(algorithm.evolve('DNSGAII', population))

func = []
for i in algorithm.evolve('DNSGAII', population):
    for j in i:
        func.append(j)



function1 = [i[0] for i in func]

function2 = [i[1] for i in func]
plt.xlabel('Function 1', fontsize=15)
plt.ylabel('Function 2', fontsize=15)
plt.scatter(function1, function2)
plt.show()

