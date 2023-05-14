from Problem import Problem

class ZDT2(Problem):

    def __init__(self, n_variables):
        """ ZDT2 is a test suite for static optimisation

        Parameters
        ----------
        n_variables : int
            Number of variables
        """
        self.n_variables = 30

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

        Adapted from: https://pymoo.org/problems/multi/zdt.html

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

        Adapted from: https://pymoo.org/problems/multi/zdt.html

        Parameters
        ----------
        x : list
            List of variables of an individual

        Returns
        -------
        float
            Calculate the value from the sub-functions g,h and return f2's value
        """
        try:
            sigma = sum(x[1:])
            g = 1 + sigma*9/(self.n_variables - 1)
            h = 1 - (self.f1(x)/g) ** 2
            return (g * h)/2
        except:
            return
