from Utils import NSGAUtils, MOEADUtils, COEAUtils
from tqdm import tqdm
import random
import numpy as np

class Evolution:

    def __init__(self, problem, n_individuals, n_generations, n_variables, min, max):
        self.nsga = NSGAUtils(problem, n_individuals, n_generations, n_variables, min, max)
        self.moead = MOEADUtils(problem, n_individuals, n_generations, n_variables, min, max)
        self.coea= COEAUtils(problem, n_individuals, n_generations, n_variables, min, max)
        self.n_individuals = n_individuals
        self.n_generations = n_generations
        self.n_variables = n_variables


    def evolve(self, name, population):
        if name == 'NSGAII':
            return self.evolveNSGAII(population)
        
        if name == 'DNSGAIIA':
            return self.evolveDNSGAIIA(population)
        
        if name == 'COEA':
            return self.evolveCOEA(population)
        
        if name == 'MOEAD':
            return self.evolveMOEAD(population)

    def evolveNSGAII(self, population:list):
        self.nsga.evaluate_objective_values(population,self.n_individuals)
        pareto = self.nsga.fast_non_dominated_sort(population)

        
        distance = [0] * len(pareto)
        
        for i in range(len(pareto)):
            distance[i] = self.nsga.crowding_distance(pareto[i])


        """CREATION OF A CHILD"""
        child = self.nsga.create_child(population)
        """END"""
                
        for i in tqdm (range (self.n_generations)):
            population.extend(child)            
            pareto = self.nsga.fast_non_dominated_sort(population)
            distance = [0] * len(pareto)

            newPopulation = []

            for j in range(len(pareto)):
                if pareto[j]:
                    if len(newPopulation) + len(pareto[j]) < self.n_individuals:
                        distance[j] = self.nsga.crowding_distance(pareto[j])
                        newPopulation.extend(pareto[j])
                else:
                    break
        

            distance[j] = self.nsga.crowding_distance(pareto[j]) 
            pareto[j].sort(key=lambda distance: distance, reverse=False) 
            
            #newPopulation.extend(pareto[j])

            returned_pareto = pareto
            population = newPopulation

            pareto = self.nsga.fast_non_dominated_sort(population)
            distance = [0] * len(pareto)
            for p in range(len(pareto)):
               distance[p] = self.nsga.crowding_distance(pareto[p])
            
            """CREATION OF A CHILD"""
            child = self.nsga.create_child(population)
            """END"""            
        
        function = []
        y = []
        for i in returned_pareto:
            for j in i:
                function.append(j)
                y.append(j[1])

        max_v = max(y) 
        min_v = min(y)         
        
        # Adapted from https://stackoverflow.com/questions/74232723/data-frame-normalization-center-0-solution-1-1
        for i in range(len(function)):
            function[i][1] = (function[i][1] - min_v) * (self.n_variables/3/(max_v - min_v))


        return function
    

    def evolveDNSGAIIA(self, population:list, n_solutions):
        self.nsga.evaluate_objective_values(population,self.n_individuals)
        pareto = self.nsga.fast_non_dominated_sort(population)
        
        distance = []
        for i in range(len(pareto)):
            distance.append(self.nsga.crowding_distance(pareto[i]))
        
        """CREATION OF A CHILD"""
        child = self.nsga.create_child(population)
        """END"""

                
        for i in tqdm (range (self.n_generations)):
            
            # Fast Changing environment
            if i%10 == 0:
                temp_population = self.nsga.generate_random_solutions(n_solutions)
                obj = self.nsga.calculate_objective_values(temp_population, n_solutions)
                population = self.nsga.replace_element(population, obj, n_solutions)


            population.extend(child)            
            pareto = self.nsga.fast_non_dominated_sort(population)
            
            newPopulation = []


            for j in range(len(pareto)):
                if pareto[j]:
                    if len(newPopulation) + len(pareto[j]) < self.n_individuals:
                        distance[j] = self.nsga.crowding_distance(pareto[j])
                        newPopulation.extend(pareto[j])
                else:
                    break


            distance[j] = self.nsga.crowding_distance(pareto[j]) 
            pareto[j].sort(key=lambda distance: distance, reverse=False) 
            
            newPopulation.extend(pareto[j][0:self.n_variables - len(newPopulation)])

            returned_pareto = pareto
            population = newPopulation
            
            """CREATION OF A CHILD"""
            child = self.nsga.create_child(population)
            """END"""            
        
        return returned_pareto

        
    def evolveCOEA(self, population, n_splits):
        # Split the population in n parts using the method
        subpopulations = self.coea.split_populations(population, n_splits)


        # Get the fitness value
        n_fitness = self.coea.get_fitness()

        newPopulation = []

        for i in range(n_fitness):
            if len(newPopulation) < self.n_individuals:
                r = random.randint(0,1)
                if r == 0 or i % 10 == 0:
                    temp = self.coea.competitive_process(subpopulations)
                    newPopulation.extend(self.coea.evaluate_objective_values(temp, len(temp)))
                    # Shuffle subpopulation individuals"""
                    random.shuffle(newPopulation)
                    # Crossover & Mutation
                    parent1 = random.choice(newPopulation)
                    parent2 = random.choice(newPopulation)
                    child = self.coea.sbx(parent1, parent2, 1)
                    child[0] = self.coea.polynomial_mutation(child[0], 1)
                    child[1] = self.coea.polynomial_mutation(child[1], 1)
                    child = self.coea.evaluate_objective_values(child,len(child))
                    newPopulation.extend(child)
                else:		
                    newPopulation.extend(self.coea.cooperative_process(subpopulations)) 			
                    child = self.coea.create_child(newPopulation)
                    newPopulation.extend(child)
            else:
                break

        #Update and Return Archive
        #newPopulation.extend(self.coea.cooperative_process(newPopulation))
        #return self.coea.evaluate_objective_values(newPopulation, len(newPopulation))

        
        # Working
        #return self.coea.objective_values


        function = []
        y = []
        for i in range(len(self.coea.objective_values)):
            function.append(self.coea.objective_values[i])
            y.append(self.coea.objective_values[i][1])
            
        max_v = max(y) 
        min_v = min(y)         
        
        # Adapted from https://stackoverflow.com/questions/74232723/data-frame-normalization-center-0-solution-1-1
        for i in range(len(function)):
            function[i][1]/=5


        return function
        
    

    def evolveMOEAD(self, population):
        self.moead.initilizeMOEAD(population)
