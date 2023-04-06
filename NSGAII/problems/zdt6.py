import math
from Problem import Problem

class ZDT6(Problem):

    def __init__(self, n_variables):
        self.n_variables = 10


    def evaluate_objective_values(self, elements):
        f1 = self.f1(elements)
        f2 = self.f2(elements)

        return f1, f2

    def f1(self, x):
        return (1 - math.exp(-4 * x[0]) * math.sin(6 * math.pi * x[0]) ** 6)

    def f2(self, x): 
        sigma = sum(x ** (0.25) for x in x[1:])
        g = 1 + 9 * sigma
        h = 1 - (self.f1(x)/g) ** 2
        return g * h
