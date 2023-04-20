import math
from Problem import Problem

class DF7(Problem):

    def __init__(self, n_generations):
        self.n_generations = n_generations


    def evaluate_objective_values(self, elements):
        f1 = self.f1(elements)
        f2 = self.f2(elements)

        return f1, f2

    def f1(self, x):
        a = 5 * math.cos(0.5 * math.pi * self.n_generations)
        temp_x = [x_i - (1 / (1 + math.exp(a * x[0] - 2.5))) ** 2 for x_i in x[1:]]   
        g = 1 + sum(temp_x)
        return g * (1 + self.n_generations) / x[0]

    def f2(self, x):
        a = 5 * math.cos(0.5 * math.pi * self.n_generations)
        temp_x = [x_i - (1 / (1 + math.exp(a * x[0] - 2.5))) ** 2 for x_i in x[1:]]   
        g = 1 + sum(temp_x)
    
        return g * (self.f1(x) / (1 + self.n_generations))

       


        
