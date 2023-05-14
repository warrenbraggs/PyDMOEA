import math
from Problem import Problem

class ZDT4(Problem):

    def __init__(self, n_variables):
        """ ZDT4 is a test suite for static optimisation

        Parameters
        ----------
        n_variables : int
            Number of variables
        """
        self.n_variables = 10


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
        """ Function 1 of the MOP

        Parameters
        ----------
        x : list
            List of variables of an individual

        Returns
        -------
        float
            First element of the individual
        """
        return x[0]

    def f2(self, x): 
        """Function 2 of the MOP

        Parameters
        ----------
        x : list
            List of variables of an individual

        Returns
        -------
        float
            Calculate value from sub-functions g and h
        """
        try:
            sigma = sum((x ** 2 - 10 * math.cos(4 * math.pi * x)) for x in x[1:])
            g = 1 + 10*(self.n_variables - 1) + sigma
            h = 1 - math.sqrt(self.f1(x)/g)
            return (g * h) / 30
        except:
            return
    
