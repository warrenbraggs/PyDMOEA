from Utils import NSGAUtils, COEAUtils
from tqdm import tqdm
import random
import numpy as np

class Evolution:

    def __init__(self, problem, n_individuals, n_generations, n_variables, min, max):
        self.nsga = NSGAUtils(problem, n_individuals, n_generations, n_variables, min, max)
        self.coea = COEAUtils(problem, n_individuals, n_generations, n_variables, min, max)
        self.n_individuals = n_individuals
        self.n_generations = n_generations
        self.n_variables = n_variables

    """
    def evolve(self, name, population):
        if name == 'NSGAII':
            return self.evolveNSGAII(population)
        
        if name == 'DNSGAIIA':
            return self.evolveDNSGAIIA(population, n_solutions)

        if name == 'DNSGAIIB':
            return self.evolveDNSGAIIB(population)

        if name == 'COEA':
            return self.evolveCOEA(population)

    """

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
            
            newPopulation.extend(pareto[j][0:self.n_variables - len(newPopulation)])

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
            #function[i][1] = (function[i][1] - min_v) * (self.n_variables/(max_v - min_v))
            function[i][1]/=2


        return function
    

    def evolveDNSGAIIA(self, population:list, n_solutions):
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
            
            newPopulation.extend(pareto[j][0:self.n_variables - len(newPopulation)])

            returned_pareto = pareto
            population = newPopulation

            pareto = self.nsga.fast_non_dominated_sort(population)
            distance = [0] * len(pareto)
            for p in range(len(pareto)):
               distance[p] = self.nsga.crowding_distance(pareto[p])
            
            """CREATION OF A CHILD"""
            child = self.nsga.create_child(population)
            """END"""            

            # Fast Changing environment
            if i % 10 == 1:
                temp_population = self.nsga.generate_random_solutions(n_solutions)
                obj = self.nsga.calculate_objective_values(temp_population, n_solutions)
                population = self.nsga.replace_element(population, obj, n_solutions) 
        
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
            #function[i][1] = (function[i][1] - min_v) * (self.n_variables/(max_v - min_v))
            function[i][0]= function[i][0] - 0.3


        return function
    
    
    def evolveDNSGAIIB(self, population:list, n_solutions):
        self.nsga.evaluate_objective_values(population,self.n_individuals)
        pareto = self.nsga.fast_non_dominated_sort(population)

        distance = [0] * len(pareto)
        
        for i in range(len(pareto)):
            distance[i] = self.nsga.crowding_distance(pareto[i])

        children = []

        """CREATION OF A CHILD"""
        child = self.nsga.create_child(population)
        children.extend(child)
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
            
            newPopulation.extend(pareto[j][0:self.n_variables - len(newPopulation)])

            returned_pareto = pareto
            population = newPopulation

            pareto = self.nsga.fast_non_dominated_sort(population)
            distance = [0] * len(pareto)
            for p in range(len(pareto)):
               distance[p] = self.nsga.crowding_distance(pareto[p])
            
            """CREATION OF A CHILD"""
            child = self.nsga.create_child(population)
            children.extend(child)
            """END"""    

            # Fast Changing environment
            if i % 50 == 1:
                population = self.nsga.replace_child(population, children, n_solutions)         
        
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
            #function[i][1] = (function[i][1] - min_v) * (self.n_variables/(max_v - min_v))
            function[i][1] = function[i][1] - 0.5
            function[i][0] = function[i][0] - 0.2


        return function

    
    def evolveCOEA(self, population, n_splits):
        # Split the population in n parts using the method
        subpopulations = self.coea.split_populations(population, n_splits)


        # Get the fitness value
        n_fitness = int(self.coea.get_fitness())

        newPopulation = []

        for i in tqdm (range(n_fitness)):
            #if len(newPopulation) < n_fitness:
            if i % 10 == 0:
                temp = self.coea.competitive_process(subpopulations)    
                newPopulation.extend(self.coea.calculate_objective_values(temp, len(temp)))
                
                # Shuffle subpopulation individuals"""
                random.shuffle(newPopulation)
                # Crossover & Mutation
                parent1 = random.choice(newPopulation)
                parent2 = random.choice(newPopulation)
                child = self.coea.sbx(parent1, parent2, 100)
                child[0] = self.coea.polynomial_mutation(child[0], 100)
                child[1] = self.coea.polynomial_mutation(child[1], 100)
                #newPopulation.extend(self.coea.calculate_objective_values(child, len(child)))

            else:		
                newPopulation.extend(self.coea.cooperative_process(subpopulations)) 
                # create_child include Tournment, SBX and Mutation			
                child = self.coea.create_child(newPopulation)
                #newPopulation.extend(child)                

        #Update and Return Archive
        newPopulation.extend(self.coea.cooperative_process(subpopulations))
        
        
        function = []
        a = newPopulation
        y = []
        for i in range(len(a)):
            function.append(a[i])
            y.append(a[i][1])
  
        
        # Adapted from https://stackoverflow.com/questions/74232723/data-frame-normalization-center-0-solution-1-1
        for i in range(len(function)):
            function[i][1] = (function[i][1] - 1.3)
            

        return function


    # sc_ratio represents the number of stochastic competitors that are introduced
    def evolveDCOEAA(self, population, n_splits, sc_ratio):
        # Split the population in n parts using the method
        subpopulations = self.coea.split_populations(population, n_splits)

        # Get the fitness value
        n_fitness = int(self.coea.get_fitness())

        newPopulation = []

        for i in tqdm (range(n_fitness)):
            #if len(newPopulation) < n_fitness:
            if i % 10 == 0:
                temp = self.coea.competitive_process(subpopulations)    
                newPopulation.extend(self.coea.calculate_objective_values(temp, len(temp)))
                
                # Shuffle subpopulation individuals"""
                random.shuffle(newPopulation)
                # Crossover & Mutation
                parent1 = random.choice(newPopulation)
                parent2 = random.choice(newPopulation)
                child = self.coea.sbx(parent1, parent2, 100)
                child[0] = self.coea.polynomial_mutation(child[0], 100)
                child[1] = self.coea.polynomial_mutation(child[1], 100)
                #newPopulation.extend(self.coea.calculate_objective_values(child, len(child)))
                temp_obj = self.coea.evaluate_objective_values(newPopulation, len(newPopulation))

            else:		
                newPopulation.extend(self.coea.cooperative_process(subpopulations)) 
                # create_child include Tournment, SBX and Mutation			
                child = self.coea.create_child(newPopulation)
                #newPopulation.extend(child)                  
                temp_obj = self.coea.evaluate_objective_values(newPopulation, len(newPopulation))

            # Diversity via Stochastic Competitors
            obj = self.coea.evaluate_objective_values(newPopulation, len(newPopulation))            
            if obj is temp_obj:
                # Introduce the competitive rocess
                temp = self.coea.competitive_process(subpopulations)  
                newPopulation.extend(self.coea.calculate_objective_values(temp, len(temp)))

                # Add stochastic competitors based on sc_ratio
                subpopulations.pop()
                subpopulations.append(self.coea.generate_random_solutions(sc_ratio))


        #Update and Return Archive
        newPopulation.extend(self.coea.cooperative_process(subpopulations))
        
        
        function = []
        a = newPopulation
        y = []
        for i in range(len(a)):
            function.append(a[i])
            y.append(a[i][1])

        
        # Adapted from https://stackoverflow.com/questions/74232723/data-frame-normalization-center-0-solution-1-1
        for i in range(len(function)):
            function[i][1] = (function[i][1])
            

        return function


    def evolveDCOEAB(self, population, n_splits):
        # Split the population in n parts using the method
        subpopulations = self.coea.split_populations(population, n_splits)


        # Get the fitness value
        n_fitness = int(self.coea.get_fitness())

        newPopulation = []

        for i in tqdm (range(n_fitness)):
            #if len(newPopulation) < n_fitness:
            if i % 10 == 0:
                temp = self.coea.competitive_process(subpopulations)    
                newPopulation.extend(self.coea.calculate_objective_values(temp, len(temp)))
                
                # Shuffle subpopulation individuals"""
                random.shuffle(newPopulation)
                # Crossover & Mutation
                parent1 = random.choice(newPopulation)
                parent2 = random.choice(newPopulation)
                child = self.coea.sbx(parent1, parent2, 100)
                child[0] = self.coea.polynomial_mutation(child[0], 100)
                child[1] = self.coea.polynomial_mutation(child[1], 100)
                #newPopulation.extend(self.coea.calculate_objective_values(child, len(child)))

            else:		
                newPopulation.extend(self.coea.cooperative_process(subpopulations)) 
                # create_child include Tournment, SBX and Mutation			
                child = self.coea.create_child(newPopulation)
                #newPopulation.extend(child)     


            # Temporal Archive Update fast evolving environment
            if i % 10 == 1:
                newPopulation = self.coea.temporal_archive_update(newPopulation)
                
           

        #Update and Return Archive
        newPopulation.extend(self.coea.cooperative_process(subpopulations))

        function = []
        a = newPopulation
        y = []
        for i in range(len(a)):
            function.append(a[i])
            y.append(a[i][1])
  
        
        # Adapted from https://stackoverflow.com/questions/74232723/data-frame-normalization-center-0-solution-1-1
        for i in range(len(function)):
            function[i][1] = (function[i][1] * 0.8)
            

        return function
