import math
from Problem import Problem

class DF1(Problem):

    def __init__(self, n_generations):
        self.n_generations = n_generations


    def evaluate_objective_values(self, elements):
        f1 = self.f1(elements)
        f2 = self.f2(elements)

        return f1, f2

    def f1(self, x):
        return x[0]

    def f2(self, x):
        v = math.sin(0.5 * math.pi * self.n_generations)
        G = abs(v)
        H = 0.75 * v + 1.25
        sigma = sum(((x - 2 - G) ** 2) for x in x[1:])
        g = 1 + sigma

        return g * (1 - ((self.f1(x) / g) ** H))

        
