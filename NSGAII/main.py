from problems.zdt1 import ZDT1
from problems.zdt2 import ZDT2
from problems.zdt3 import ZDT3

from DynamicUtils import DynamicUtils
from Evolution import Evolution

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.problems import get_problem
from pymoo.indicators.igd import IGD
import pygmo as pg   

import matplotlib.pyplot as plt


""" Definition of parameters used for NSGAII

Parameters:
-----------
n_individuals: int
n_generations: int
n_variables: int
min: int
max: int
"""
n_individuals = 100 #100
n_generations = 200 #200
n_variables = 30
min = 0
max = 1


zdt2 = ZDT2(n_variables)
dynamic_evolution = DynamicUtils(zdt2, n_individuals, n_generations, n_variables, min, max)
nsgaii_zdt2 = Evolution(zdt2, n_individuals, n_generations, n_variables, min, max)

# zdt3 = ZDT3(n_variables)
# dynamic_evolution = DynamicUtils(zdt3, n_individuals, n_generations, n_variables, min, max)
# nsgaii_zdt3 = Evolution(zdt3, n_individuals, n_generations, n_variables, min, max)


# Generation of the population and initialization
population = []
for i in range(n_individuals):
    population = dynamic_evolution.generate_random_solutions()

function = []
for i in nsgaii_zdt2.evolveNSGAII(population):
    for j in i:
        function.append(j)

# Optimal Pareto Front for ZDT1
problem = get_problem("zdt2")
x, y = problem.pareto_front().T

# Optimal Pareto Front for ZDT2
# problem = get_problem("zdt2")
# x, y = problem.pareto_front().T

plt.plot(x, y, 'ro')

# Plotting
function1 = [i[0] for i in function]
function2 = [i[1] for i in function]
plt.xlabel('Function 1', fontsize=15)
plt.ylabel('Function 2', fontsize=15)
plt.plot(function1, function2, 'bo')
plt.xlim([0, 1])
plt.ylim([-1, 10])
plt.show()

# Performance Indicators

ind = IGD(function)
print("IGD", ind(function1))
