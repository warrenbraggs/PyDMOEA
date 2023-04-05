import numpy as np

from problems.zdt1 import ZDT1
from problems.zdt2 import ZDT2
from problems.zdt3 import ZDT3

from DynamicUtils import DynamicUtils
from Evolution import Evolution

from pymoo.problems import get_problem

from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV

from platypus import NSGAII, NSGAIII, DTLZ2, Hypervolume, experiment, calculate, display

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


problem = ZDT1(n_variables)
dynamic_evolution = DynamicUtils(problem, n_individuals, n_generations, n_variables, min, max)
nsgaii = Evolution(problem, n_individuals, n_generations, n_variables, min, max)

# Optimal Pareto Front for ZDT1
zdt1 = get_problem("zdt1")
x, y = zdt1.pareto_front().T


# Generation of the population and initialization
population = []
for i in range(n_individuals):
    population = dynamic_evolution.generate_random_solutions()

function = []
for i in nsgaii.evolveNSGAII(population):
    for j in i:
        function.append(j)


# Plotting
function1 = [i[0] for i in function]
function2 = [i[1] for i in function]
plt.xlabel('Function 1', fontsize=15)
plt.ylabel('Function 2', fontsize=15)
plt.plot(function1, function2, 'bo')
plt.plot(x, y, 'ro')
plt.xlim([0, 1])
plt.ylim([-1, 10])
#plt.show()

# Performance Indicators
function = np.array(function)
# igd = IGD(zdt1.pareto_front())
# print("IGD", igd(function))

hv = HV(zdt1.pareto_front())
print("HV", hv(function))

# hyp = Hypervolume(minimum=[0, 0], maximum=[11, 11])
# print(hyp.calculate(function))
