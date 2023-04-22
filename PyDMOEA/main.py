import numpy as np
import matplotlib.pyplot as plt

from Utils import NSGAUtils, MOEADUtils, COEAUtils
from Evolution import Evolution

from problems.zdt1 import ZDT1
from problems.zdt2 import ZDT2
from problems.zdt4 import ZDT4  
from problems.bnh import BNH    # not working
from problems.df1 import DF1
from problems.df2 import DF2
from problems.df3 import DF3
from problems.df5 import DF5    
from problems.df7 import DF7    # not working
from pymoo.problems import get_problem


from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV
from pymoo.visualization.scatter import Scatter



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
n_individuals = 100 
n_generations = 200 
n_variables = 2
min = 0
max = 1

# ZDT1, ZDT2 for STATIC: 30 objectives
# ZDT4 for STATIC: 10 objectives
# DF1, DF2, DF3, DF5 for DYNAMIC: 2 objectives (used in pymoo)


# Initialisation
problem = DF2(n_generations)
algorithm = NSGAUtils(problem, n_individuals, n_generations, n_variables, min, max)
evolution = Evolution(problem, n_individuals, n_generations, n_variables, min, max)

# Optimal Pareto Front for testing a problem
pf = get_problem("df2")
x, y = pf.pareto_front().T



# Generation of the population and initialization
population = algorithm.generate_random_solutions(n_individuals)

# Evolution of the algorith given the problem
# Number of splits for COEA (10 suggested)
# Number of changes for Dynamic (30 suggested)
function = evolution.evolveDNSGAIIB(population, 20)


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
plt.plot(f1, f2, 'bo', label='NSGAII')
plt.legend(loc="upper right")
plt.xlim([0, 1])
plt.ylim([-1, 7])
plt.show()

