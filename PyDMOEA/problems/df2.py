import math
from Problem import Problem

class DF2(Problem):

    def __init__(self, n_generations):
        self.n_variables = 2
        self.n_generations = n_generations


    def evaluate_objective_values(self, elements):
        f1 = self.f1(elements)
        f2 = self.f2(elements)

        return f1, f2

    def f1(self, x):
        try:
            v = math.sin(0.5 * math.pi * self.n_generations)
            G = abs(v)
            index = int((self.n_variables - 1) * G)
            return (x[index])
        except:
            return

    def f2(self, x):
        try:
            v = math.sin(0.5 * math.pi * self.n_generations)
            G = abs(v)
            r = int((self.n_variables - 1) * G)
            not_r = [k for k in range(self.n_variables) if k != r]
            index = max(not_r)
            
            sigma = sum((x - G) ** 2 for x in x[:index])
            g = 1 + sigma

            return (g * (1 - math.sqrt(self.f1(x)/g)))
        except:
            return

        
