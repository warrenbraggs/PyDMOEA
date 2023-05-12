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



def get_mean(list_values):
    """ Calculate the mean values for MIGD and MHV (Performance Indicators)

    Parameters
    ----------
    list_values : float list
        list of optimal set of solutions (x,y)

    Returns
    -------
    float list
        mean values of the optimal set of solutions
    """
    value = 0
    for i in list_values:        
        value = value + i  
    return value/len(list_values)




""" Definition of parameters used for testing an algorithm based on the problem specification

Parameter settings guideline:
STATIC EVOLUTION (ZDT1, ZDT2): 30 variables
STATIC EVOLUTION (ZDT4): 10 variables
DYNAMIC EVOLUTION (DF1, DF2, DF3, DF5): 2 variables 

Parameters
----------
n_individuals : int
n_generations : int
n_variables : int
min : int
max : int
"""
n_individuals = 100 
n_generations = 200
n_variables = 30
min = 0
max = 1

# Initialisation of the problem 
problem = ZDT1(n_generations)
# Initialisation of the algorithm (NSGAII, COEA, DNSGAIIA, DNSGAIIB, DCOEAA, DCOEAB)
algorithm = NSGAUtils(problem, n_individuals, n_generations, n_variables, min, max)
# Initialisation of the evolution (static/dynamic) 
evolution = Evolution(problem, n_individuals, n_generations, n_variables, min, max)


# Definition of the Pareto Optimal Front by pymoo
pf = get_problem("zdt1")
x, y = pf.pareto_front().T


# Start the stopwatch for measuring the time used by the algorithm considered
start_time = time.time()


# Generation of the population and initialisation
population = algorithm.generate_random_solutions(n_individuals)

"""
Additional parameter settings guideline:
COEA: number of splits (n_splits) = 10
DNSGAIIA/B: number of changes (n_solutions) = 30
DCOEAA: number of splits (n_splits) = 10, stocastic process ratio (sc ratio) = 1
DCOEAB: number of splits (n_splits) = 10
"""
# Start evolution
function = evolution.evolveCOEA(population, 10)

# End the stopwatch for measuring the time
end_time = time.time()
# Time calculation
time = end_time - start_time
# Display time taken
print(time)


# Convert the list into numpy array
function = np.array(function)
function_mean_value = get_mean(function)

# Performance Indicators
migd = IGD(pf.pareto_front())
print("MIGD", migd(function_mean_value)/function_mean_value[1])
mhv = HV(function_mean_value)
print("MHV", mhv(pf.pareto_front())/np.prod(function_mean_value))


# Plotting
f1 = [i[0] for i in function]
f2 = [i[1] for i in function]
# Plot the Pareto Optimal Front
plt.plot(x, y, 'ro', label='Pareto Front')
# Plot the algorithm desired
plt.plot(f1, f2, 'bo', label='Algorithm')
plt.legend(loc="upper right")
plt.xlim([0, 1])
plt.ylim([-1, 7])
plt.show()

