import numpy as np

from problems.zdt1 import ZDT1
from problems.zdt2 import ZDT2
from pymoo.problems import get_problem

from DynamicUtils import DynamicUtils
from Evolution import Evolution

from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV

import matplotlib.pyplot as plt


def get_mean(list):
    value = 0
    for i in list:
        value = value + i
    return value/len(list)

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

# Optimal Pareto Front for a Test Problem
pf = get_problem("zdt1")
x, y = pf.pareto_front().T


# Generation of the population and initialization
population = []
for i in range(n_individuals):
    population = dynamic_evolution.generate_random_solutions()

function = []
for i in nsgaii.evolveNSGAII(population):
    for j in i:
        function.append(j)


# Normalize function [0,1]
function = np.array(function)
f = (function - np.min(function))/(np.max(function)-np.min(function))


# Plotting
f1 = [i[0] for i in function]
f2 = [i[1] for i in function]

plt.plot(x, y, 'ro', label='Pareto Front')
plt.plot(f1, f2, 'bo', label='NSGAII')
plt.legend(loc="upper left")
plt.xlim([0, 1])
plt.ylim([-1, 10])
plt.show()

# Performance Indicators

f_mean = get_mean(f)

migd = IGD(pf.pareto_front())
print("MIGD", migd(f_mean))

mhv = HV(f_mean)
print("MHV", mhv(pf.pareto_front()))
