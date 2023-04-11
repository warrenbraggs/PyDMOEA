from Problem import Problem

class ZDT2(Problem):

    def __init__(self, n_variables):
        self.n_variables = 30

    def evaluate_objective_values(self, elements):
        f1 = self.f1(elements)
        f2 = self.f2(elements)

        return f1, f2

    def f1(self, x):
        return x[0]

    def f2(self, x):
        try:
            sigma = sum(x[1:])
            g = 1 + sigma*9/(self.n_variables - 1)
            h = 1 - (self.f1(x)/g) ** 2
            return g * h
        except:
            return