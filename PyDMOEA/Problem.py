from abc import abstractmethod, ABC

class Problem:
    def __init__(self, n_variables):
        """ Problem is an abstract class that defines the Multi-Objective Problem (MOP) and Dynamic Multi-Objective Problem (DMOP) used by the algorithms

        Parameters
        ----------
        n_variables : int
            Number of variables
        """
        self.n_variables = n_variables
        self.min = min
        self.max = max

    
    @abstractmethod
    def evaluate_objective_values(self, elements):
        """ Evaluate the objective values of an individual

        Parameters
        ----------
        elements : list
            List of variables of an individual
        """
        pass


    @abstractmethod
    def f1(self, x):
        """ Function 1 determined by the specifications of the problem

        Parameters
        ----------
        x : list
            List of variables
        """
        pass

    @abstractmethod
    def f2(self, x):
        """ Function 2 determined by the specifications of the problem

        Parameters
        ----------
        x : list
            List of variables
        """
        pass