import math
from Problem import Problem

class DF3(Problem):

    def __init__(self, n_generations):
        self.n_generations = n_generations


    def evaluate_objective_values(self, elements):
        f1 = self.f1(elements)
        f2 = self.f2(elements)

        return f1, f2

    def f1(self, x):
        return x[0]

    def f2(self, x):
        try:
            G = math.sin(0.5 * math.pi * self.n_generations)
            H = G + 1.5

            g = 1 + (sum(x[1:]) - G - self.f1(x) ** H) ** 2
            return (g * (1 - (self.f1(x) / g) ** H)) * 1.5
        except:
            return
        

        

        
