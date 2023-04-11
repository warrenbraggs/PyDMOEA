import math
from Problem import Problem

class BNH(Problem):

    def __init__(self, n_variables):
        self.n_variables = 2


    def evaluate_objective_values(self, elements):
        f1 = self.f1(elements)
        f2 = self.f2(elements)
        c1 = self.c1(elements)
        c2 = self.c2(elements)

        return f1, f2

    def f1(self, x):
        for i in range(len(x)-1):
            if x[i] >= 0 and x[i] <= 5:
                return (4 * x[i] ** 2 + 4 * x[i+1] ** 2)
        

    def f2(self, x):
        for i in range(len(x)-1):
            if x[i] >= 0 and x[i] <= 3:
                return ((x[0]- 5) ** 2 + (x[1] - 5) ** 2)
        

    def c1(self, x):
        return ((1 / 25) * ((x[0] - 5) ** 2 + x[1] ** 2 - 25))
    
    def c2(self, x):
        return (-1 / 7.7 * ((x[0] - 8) ** 2 + (x[1] + 3) ** 2 - 7.7))

