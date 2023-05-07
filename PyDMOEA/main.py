import numpy as np
import matplotlib.pyplot as plt

import time

from Utils import NSGAUtils, COEAUtils
from Evolution import Evolution

from problems.zdt1 import ZDT1
from problems.zdt2 import ZDT2
from problems.zdt4 import ZDT4  
from problems.df1 import DF1
from problems.df2 import DF2
from problems.df3 import DF3
from problems.df5 import DF5    
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

# STATIC EVOLUTION (ZDT1, ZDT2): 30 variables
# STATIC EVOLUTION (ZDT4): 10 variables
# DYNAMIC EVOLUTION (DF1, DF2, DF3, DF5): 2 variables 

n_individuals = 100 
n_generations = 200 
n_variables = 2
min = 0
max = 1

# Initialisation
problem = DF5(n_generations)
algorithm = COEAUtils(problem, n_individuals, n_generations, n_variables, min, max)
evolution = Evolution(problem, n_individuals, n_generations, n_variables, min, max)

# Optimal Pareto Front for testing a problem
pf = get_problem("DF5")
x, y = pf.pareto_front().T


# Start the stopwatch for measuring the time
start_time = time.time()


# Generation of the population and initialization
population = algorithm.generate_random_solutions(n_individuals)


# Evolution of the algorith given the problem
# COEA: number of splits = 10
# DNSGAIIA/B: number of changes = 30
# DCOEAA: number of splits = 10, sc ratio = 1
# DCOEAB: number of splits = 10
function = evolution.evolveDCOEAB(population, 10)


# End the stopwatch for measuring the time
end_time = time.time()

time = end_time - start_time
print(time)


# Performance Indicators
function = np.array(function)
function_mean_value = get_mean(function)

migd = IGD(pf.pareto_front())
print("MIGD", migd(function_mean_value)/function_mean_value[1])
mhv = HV(function_mean_value)
print("MHV", mhv(pf.pareto_front())/np.prod(function_mean_value))


# Plotting
f1 = [i[0] for i in function]
f2 = [i[1] for i in function]
plt.plot(x, y, 'ro', label='Pareto Front')
plt.plot(f1, f2, 'bo', label='DCOEAB')
plt.legend(loc="upper right")
plt.xlim([0, 1])
plt.ylim([-1, 7])
plt.show()

