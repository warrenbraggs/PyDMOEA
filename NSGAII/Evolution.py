from DynamicUtils import DynamicUtils
import numpy as np
from tqdm import tqdm

class Evolution:

    def __init__(self, problem, n_individuals=100, n_generations=10):
        self.genetic = DynamicUtils(problem, n_individuals)
        self.n_generations = n_generations


    def evolve(self, name, population):
        if name == 'DNSGAII':
            return self.evolveDNSGAII(population)
        
        if name == 'COEA':
            return self.evolveCOEA(population)
            

    def temp(self, parent):
        
        pareto = self.genetic.fast_non_dominated_sort(parent, [])
        print('Initial population', pareto)
        parent = self.genetic.check_layers(pareto)
        print('Initial parent', parent)

        for i in range (self.n_generations):
            child = []
            print('Round', i)

            newParent = self.genetic.binary_tournament_selection(parent)
            print('Tournement selection', newParent)
            
            # nc used is 1 as suggested in pymoo
            size = len(newParent)//2
            for i in range(0, size):
                temp = self.genetic.sbx(newParent[i], newParent[i+1], 1)
                print('SBX done', temp)
                child.extend(temp)
            child = self.genetic.polynomial_mutation(child, 5)
            print('Polynomial Mut done', child)

            print('Parent ready for next pareto', parent)

            pareto = self.genetic.fast_non_dominated_sort(parent, child)
            parent = self.genetic.check_layers(pareto)
            print('Fast non dominated sort done ', parent)

        return parent
    

    def evolveDNSGAII(self, population:list):
        objective_values = self.genetic.init_population(population)
        pareto = self.genetic.fast_non_dominated_sort(population)
        parent = self.genetic.check_layers(pareto)


        for i in tqdm (range (self.n_generations)):
            child = []

            while len(child) < len(parent):
                parent1 = self.genetic.tournament_selection(parent)
                parent2 = parent1

                while parent1 == parent2:
                    parent2 = self.genetic.tournament_selection(parent)
                                       
                
                temp = self.genetic.sbx(parent1, parent2, 10)
                
                c1 = self.genetic.init_population(temp)
                c2 = self.genetic.init_population(temp)
                c1 = self.genetic.polynomial_mutation(c1, 5)
                c2 = self.genetic.polynomial_mutation(c2, 5)

                child.append(c1)
                child.append(c2)
            
            pareto = self.genetic.fast_non_dominated_sort([child, parent])
            parent = self.genetic.check_layers(pareto)

            print(pareto)


        return pareto

        
    def evolveCOEA(self, population):
        self.genetic.cooperative_competitive(population, 10)

