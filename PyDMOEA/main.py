import numpy as np

from problems.zdt1 import ZDT1
from problems.zdt2 import ZDT2
from problems.zdt3 import ZDT3  # not working
from problems.zdt4 import ZDT4  # not working
from problems.zdt6 import ZDT6  # not working
from pymoo.problems import get_problem

from Utils import Utils
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
dynamic_evolution = Utils(problem, n_individuals, n_generations, n_variables, min, max)
algorithm = Evolution(problem, n_individuals, n_generations, n_variables, min, max)

# Optimal Pareto Front for a Test Problem
pf = get_problem("zdt1")
x, y = pf.pareto_front().T


# Generation of the population and initialization

population = dynamic_evolution.generate_random_solutions(n_individuals)
population1 = dynamic_evolution.generate_random_solutions(n_individuals)

nsgaii_function = []
dnsgaiia_function = []


for i in algorithm.evolveNSGAII(population):
    for j in i:
        nsgaii_function.append(j)

for i in algorithm.evolveDNSGAIIA(population1, 10):
    for j in i:
        dnsgaiia_function.append(j)


# Normalize function [0,1]
nsgaii_f = (nsgaii_function - np.min(nsgaii_function))/(np.max(nsgaii_function)-np.min(nsgaii_function))
dnsgaiia_f = (dnsgaiia_function - np.min(dnsgaiia_function))/(np.max(dnsgaiia_function)-np.min(dnsgaiia_function))

# Plotting
f1_nsgaii = [i[0] for i in nsgaii_function]
f2_nsgaii = [i[1] for i in nsgaii_function]
f1_dnsgaiia = [i[0] for i in dnsgaiia_function]
f2_dnsgaiia = [i[1] for i in dnsgaiia_function]

plt.plot(x, y, 'ro', label='Pareto Front')
plt.plot(f1_nsgaii, f2_nsgaii, 'bo', label='NSGAII')
plt.plot(f1_dnsgaiia, f2_dnsgaiia, 'go', label='DNSGAIIA')
plt.legend(loc="upper right")
plt.xlim([0, 1])
plt.ylim([-1, 12])
plt.show()

# Performance Indicators
nsgaii_function_mean = get_mean(nsgaii_f)
dnsgaiia_function_mean = get_mean(dnsgaiia_f)

migd = IGD(pf.pareto_front())
print("MIGD", migd(nsgaii_function_mean))

mhv = HV(nsgaii_function_mean)
print("MHV", mhv(pf.pareto_front()))


migd = IGD(pf.pareto_front())
print("MIGD", migd(dnsgaiia_function_mean))

mhv = HV(dnsgaiia_function_mean)
print("MHV", mhv(pf.pareto_front()))

