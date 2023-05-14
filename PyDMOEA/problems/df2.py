import math
from Problem import Problem

class DF2(Problem):

    def __init__(self, n_generations):
        """ DF2 is a test suite for dynamic optimisation

        Parameters
        ----------
        n_generations : int
            Number of generations/iterations
        """
        self.n_variables = 2
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
            Calculate v, G, index and return f1's value
        """
        try:
            v = math.sin(0.5 * math.pi * self.n_generations)
            G = abs(v)
            index = int((self.n_variables - 1) * G)
            return (x[index])
        except:
            return

    def f2(self, x):
        """Function 2 of the DMOP

        Adapted from: https://github.com/anyoptimization/pymoo/blob/main/pymoo/problems/dynamic/df.py

        Parameters
        ----------
        x : list
            List of variables of an individual

        Returns
        -------
        float
            Calculate the value from the sub-functions v, G, r, not_r, sigma, g and return f2's value
        """
        try:
            v = math.sin(0.5 * math.pi * self.n_generations)
            G = abs(v)
            r = int((self.n_variables - 1) * G)
            not_r = [k for k in range(self.n_variables) if k != r]
        
            sigma = sum((x - G) ** 2 for x in x[not_r[0]:])
            g = 1 + sigma

            return (g * (1 - math.sqrt(self.f1(x)/g)))
        except:
            return

        
