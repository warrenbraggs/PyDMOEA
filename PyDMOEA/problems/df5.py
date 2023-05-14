import math
from Problem import Problem

class DF5(Problem):

    def __init__(self, n_generations):
        """ DF5 is a test suite for dynamic optimisation

        Parameters
        ----------
        n_generations : int
            Number of generations/iterations
        """
        self.n_generations = n_generations


    def evaluate_objective_values(self, elements):
        """ Evaluate the objective values of an individual given the variables

        Parameters
        ----------
        elements : list
            List of variables

        Returns
        -------
        list
            Objective value
        """
        f1 = self.f1(elements)
        f2 = self.f2(elements)

        return f1, f2

    def f1(self, x):
        """ Function 1 of the DMOP

        Adapted from: https://github.com/anyoptimization/pymoo/blob/main/pymoo/problems/dynamic/df.py

        Parameters
        ----------
        x : list
            List of variables of an individual

        Returns
        -------
        float
            Calculate G, w, g and return f1's value
        """
        try:
            G = math.sin(0.5 * math.pi * self.n_generations)
            w = math.floor(10 * G)
            g = 1 + sum((x_i - G) ** 2 for x_i in x[1:])
            return (g * (x[0] + 0.02 * math.sin(w * math.pi * x[0])))
        except:
            return


    def f2(self, x):
        """ Function 2 of the DMOP

        Adapted from: https://github.com/anyoptimization/pymoo/blob/main/pymoo/problems/dynamic/df.py

        Parameters
        ----------
        x : list
            List of variables of an individual

        Returns
        -------
        float
            Calculate G, w, g and return f2's value
        """
        try:
            G = math.sin(0.5 * math.pi * self.n_generations)
            w = math.floor(10 * G)
            g = 1 + sum((x_i - G) ** 2 for x_i in x[1:])
            return (g * (1 - x[0] + 0.02 * math.sin(w * math.pi * x[0]))) * 2
        except:
            return

       


        
