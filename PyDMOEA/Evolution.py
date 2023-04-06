from DynamicUtils import DynamicUtils
from tqdm import tqdm

class Evolution:

    def __init__(self, problem, n_individuals, n_generations, n_variables, min, max):
        self.genetic = DynamicUtils(problem, n_individuals, n_generations, n_variables, min, max)
        self.n_individuals = n_individuals
        self.n_generations = n_generations
        self.n_variables = n_variables


    def evolve(self, name, population):
        if name == 'NSGAII':
            return self.evolveNSGAII(population)
        
        if name == 'COEA':
            return self.evolveCOEA(population)
            

    def evolveNSGAII(self, population:list):
        self.genetic.evaluate_objective_values(population,self.n_individuals)
        pareto = self.genetic.fast_non_dominated_sort(population)
        
        distance = []
        for i in range(len(pareto)):
            distance.append(self.genetic.crowding_distance(pareto[i]))
        
        """CREATION OF A CHILD"""
        child = self.genetic.create_child(population)
        """END"""

        returned_population = None
                
        for i in tqdm (range (self.n_generations)):
            population.extend(child)            
            pareto = self.genetic.fast_non_dominated_sort(population)
            
            newPopulation = []

            # while len(newPopulation) + len(pareto[index]) < self.n_individuals:
            #     self.genetic.crowding_distance(pareto[index])
            #     newPopulation.extend(pareto[index])
            #     if pareto[index]:
            #         index += 1
            #     else:
            #         break

            for j in range(len(pareto)):
                if pareto[j]:
                    if len(newPopulation) + len(pareto[j]) < self.n_individuals:
                        distance[j] = self.genetic.crowding_distance(pareto[j])
                        newPopulation.extend(pareto[j])
                else:
                    break


            distance[j] = self.genetic.crowding_distance(pareto[j]) 
            pareto[j].sort(key=lambda distance: distance, reverse=False) 
            
            newPopulation.extend(pareto[j][0:self.n_variables - len(newPopulation)])

            returned_pareto = pareto
            population = newPopulation

            # pareto = self.genetic.fast_non_dominated_sort(population)
            # for p in range(len(pareto)):
            #    distance[p] = self.genetic.crowding_distance(pareto[p])
            
            """CREATION OF A CHILD"""
            child = self.genetic.create_child(population)
            """END"""            
        
        return returned_pareto

        
    def evolveCOEA(self, population):
        self.genetic.cooperative_competitive(population, 10)

