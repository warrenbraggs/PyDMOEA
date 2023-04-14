import numpy as np
from statistics import mean
import matplotlib.pyplot as plt

from Utils import NSGAUtils, MOEADUtils, COEAUtils
from Evolution import Evolution

from problems.zdt1 import ZDT1
from problems.zdt2 import ZDT2
from problems.zdt3 import ZDT3  # not working
from problems.zdt4 import ZDT4  # not working
from problems.zdt6 import ZDT6  # not working
from problems.bnh import BNH    # need to improve MHV
from pymoo.problems import get_problem

from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV


def get_mean(list):
    value = 0
    for i in list:
        value = value + i
    return value/len(list)

""" Definition of parameters used for testing an algorithm based on the problem specification

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
n_variables = 2    #2
min = 0
max = 1


# Initialisation
problem = ZDT1(n_variables)
algorithm = COEAUtils(problem, n_individuals, n_generations, n_variables, min, max)
evolution = Evolution(problem, n_individuals, n_generations, n_variables, min, max)

# Optimal Pareto Front for testing a problem
pf = get_problem("zdt1")
x, y = pf.pareto_front().T


# Generation of the population and initialization
population = algorithm.generate_random_solutions(n_individuals)

# Evolution of the algorith given the problem
function = evolution.evolveCOEA(population,10)


# Performance Indicators
function = np.array(function)
function_mean_value = get_mean(function)

migd = IGD(pf.pareto_front())
print("MIGD", migd(function_mean_value)/np.prod(function_mean_value))
mhv = HV(function_mean_value)
print("MHV", mhv(pf.pareto_front())/np.prod(function_mean_value))



# Plotting
f1 = [i[0] for i in function]
f2 = [i[1] for i in function]
plt.plot(x, y, 'ro', label='Pareto Front')
plt.plot(f1, f2, 'bo', label='NSGAII')
plt.legend(loc="upper right")
plt.xlim([0, 1])
plt.ylim([-1, 10])
plt.show()
