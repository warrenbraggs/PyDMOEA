from DynamicUtils import DynamicUtils
import numpy as np
from tqdm import tqdm

class Evolution:

    def __init__(self, problem, n_individuals=100, n_generations=10):
        self.genetic = DynamicUtils(problem, n_individuals)
        self.n_individuals = n_individuals
        self.n_generations = n_generations


    def evolve(self, name, population):
        if name == 'DNSGAII':
            return self.evolveDNSGAII(population)
        
        if name == 'COEA':
            return self.evolveCOEA(population)
            

    def temp(self, population:list):
        objective_values = self.genetic.init_population(population,10)
        pareto = self.genetic.fast_non_dominated_sort(population)
        print(pareto)
        #parent = self.genetic.check_layers(pareto)

        for i in range(len(pareto)-1):
            self.genetic.crowding_distance(pareto[i])
        
        for i in tqdm (range (self.n_generations)):
            child = []

            while len(child) < len(population):
                parent1 = self.genetic.tournament_selection(population)
                parent2 = parent1

                while parent1 == parent2:
                    parent2 = self.genetic.tournament_selection(population)
                        
                
                child = self.genetic.sbx(parent1[0], parent2[0], 10)
                self.genetic.polynomial_mutation(child[0], 5)
                self.genetic.polynomial_mutation(child[1], 5)
                
                # Init population + append children objectives to population objectives
                self.genetic.init_population(child,2)

                print('Pop', population , '\n')
                print('child', child, '\n')
                
                child = population[2].extend(child)
                print('New Child', child)
                break
            break
            
            pareto = self.genetic.fast_non_dominated_sort(child)
            #parent = self.genetic.check_layers(pareto)
        
    

    def evolveDNSGAII(self, population:list):
        objective_values = self.genetic.init_population(population,self.n_individuals)
        pareto = self.genetic.fast_non_dominated_sort(population)
        print(pareto)
        #parent = self.genetic.check_layers(pareto)

        for i in range(len(pareto)-1):
            self.genetic.crowding_distance(pareto[i])
        
        
        """CREATION OF A CHILD"""
        child = []
        while len(child) < len(population):
            parent1 = self.genetic.tournament_selection(population)
            parent2 = parent1

            while parent1 == parent2:
                parent2 = self.genetic.tournament_selection(population)
                    
            
            temp_child = self.genetic.sbx(parent1[0], parent2[0], 30)
            self.genetic.polynomial_mutation(temp_child[0], 5)
            self.genetic.polynomial_mutation(temp_child[1], 5)
            
            # Init population + append children objectives to population objectives
            self.genetic.init_population(temp_child,2)

            child.append(temp_child)

        """END"""

        returned_population = None
        
        for i in tqdm (range (self.n_generations)):
            population.extend(child)
            self.genetic.fast_non_dominated_sort(population)
            
            newPopulation = []
            index = 0

            while len(newPopulation) + len(pareto[index]) < 10:
                self.genetic.crowding_distance(pareto[index])
                newPopulation.extend(pareto[index])
                index += 1

            self.genetic.crowding_distance(pareto[index])
            # TOO IMPLEMENT
            #pareto[index].sort(key=lambda individual: individual.crowding_distance, reverse=True) 

            newPopulation.extend(pareto[index][0:30 - len(newPopulation)])

            returned_population = population
            returned_pareto = pareto
            population = newPopulation

            self.genetic.fast_non_dominated_sort(population)
            for i in range(len(pareto)-1):
                self.genetic.crowding_distance(pareto[i])
            
            """CREATION OF A CHILD"""
            child = []
            while len(child) < len(population):
                parent1 = self.genetic.tournament_selection(population)
                parent2 = parent1

                while parent1 == parent2:
                    parent2 = self.genetic.tournament_selection(population)
                        
                
                temp_child = self.genetic.sbx(parent1[0], parent2[0], 30)
                self.genetic.polynomial_mutation(temp_child[0], 5)
                self.genetic.polynomial_mutation(temp_child[1], 5)
                
                # Init population + append children objectives to population objectives
                self.genetic.init_population(temp_child,2)

                child.append(temp_child)

            """END"""            

        return returned_pareto

        
    def evolveCOEA(self, population):
        self.genetic.cooperative_competitive(population, 10)

