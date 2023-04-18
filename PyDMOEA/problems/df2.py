import math
from Problem import Problem

class DF2(Problem):

    def __init__(self, n_generations):
        self.n_variables = 30
        self.n_generations = n_generations


    def evaluate_objective_values(self, elements):
        f1 = self.f1(elements)
        f2 = self.f2(elements)

        return f1, f2

    def f1(self, x):
        v = math.sin(0.5 * math.pi * self.n_generations)
        G = abs(v)
        index = int((self.n_variables - 1) * G)
        return x[index]

    def f2(self, x):
        v = math.sin(0.5 * math.pi * self.n_generations)
        G = abs(v)
        r = int((self.n_variables - 1) * G)
        not_r = [k for k in range(self.n_variables) if k != r]

        sigma = sum((x[:,not_r] - G) ** 2)
        g = 1 + sigma

        return g * (1 - math.sqrt(self.f1(x)/g))

        
