from abc import abstractmethod, ABC

import random 

class Problem:
    """TODO: add documentation """
    def __init__(self, n_variables):
        self.n_variables = n_variables
        self.min = min
        self.max = max

    
    @abstractmethod
    def evaluate_objective_values(self, elements):
        """TODO: add documentation """
        pass


    @abstractmethod
    def f1(self, x):
        """TODO: add documentation """
        pass

    @abstractmethod
    def f2(self, x):
        """TODO: add documentation """
        pass

    @abstractmethod
    def perfect_pareto_front(self):
        pass
