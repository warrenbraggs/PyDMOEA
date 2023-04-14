from Utils import NSGAUtils, MOEADUtils, COEAUtils
from tqdm import tqdm
import random

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
        
        return returned_pareto
    

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
                print('Hello')
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

        print(subpopulations, '\n')

        # Get the fitness value
        n_fitness = self.coea.get_fitness()

        newPopulation = []

        for i in range(n_fitness):
            if len(newPopulation) < self.n_individuals:
                r = random.randint(0,1)
                if r == 0 or i % 10 == 0:
                    newPopulation.extend(self.coea.competitive_process(subpopulations))
                    # Shuffle subpopulation individuals"""
                    random.shuffle(newPopulation)
                    # """CALL: CROSSOVER"""
                    # """CALL: MUTATION"""
                    child = self.coea.create_child(newPopulation)
                    newPopulation.extend(child)
                else:					
                    # newPopulation.extend(self.cooperative_process(subpopulations)) 			
                    # child = self.create_child(newPopulation)
                    # newPopulation.extend(child)
                    print('Hello')
            else:
                break

        #Update and Return Archive
        #return self.cooperative_process(newPopulation)
        return newPopulation


    def evolveMOEAD(self, population):
        self.moead.initilizeMOEAD(population)
