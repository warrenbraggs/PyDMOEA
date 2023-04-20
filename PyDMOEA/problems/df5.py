import math
from Problem import Problem

class DF5(Problem):

    def __init__(self, n_generations):
        self.n_generations = n_generations


    def evaluate_objective_values(self, elements):
        f1 = self.f1(elements)
        f2 = self.f2(elements)

        return f1, f2

    def f1(self, x):
        G = math.sin(0.5 * math.pi * self.n_generations)
        w = math.floor(10 * G)
        g = 1 + sum((x_i - G) ** 2 for x_i in x[1:])
        return (g * (x[0] + 0.02 * math.sin(w * math.pi * x[0])))


    def f2(self, x):
        G = math.sin(0.5 * math.pi * self.n_generations)
        w = math.floor(10 * G)
        g = 1 + sum((x_i - G) ** 2 for x_i in x[1:])
        return (g * (1 - x[0] + 0.02 * math.sin(w * math.pi * x[0])))

       


        
