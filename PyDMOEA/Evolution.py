from Utils import Utils
from tqdm import tqdm

class Evolution:

    def __init__(self, problem, n_individuals, n_generations, n_variables, min, max):
        self.genetic = Utils(problem, n_individuals, n_generations, n_variables, min, max)
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
            

    def evolveNSGAII(self, population:list):
        self.genetic.evaluate_objective_values(population,self.n_individuals)
        pareto = self.genetic.fast_non_dominated_sort(population)

        
        distance = [0] * len(pareto)
        
        for i in range(len(pareto)):
            distance[i] = self.genetic.crowding_distance(pareto[i])


        """CREATION OF A CHILD"""
        child = self.genetic.create_child(population)
        """END"""
                
        for i in tqdm (range (self.n_generations)):
            population.extend(child)            
            pareto = self.genetic.fast_non_dominated_sort(population)
            distance = [0] * len(pareto)

            newPopulation = []

            for j in range(len(pareto)):
                if pareto[j]:
                    if len(newPopulation) + len(pareto[j]) < self.n_individuals:
                        distance[j] = self.genetic.crowding_distance(pareto[j])
                        newPopulation.extend(pareto[j])
                else:
                    break
        

            distance[j] = self.genetic.crowding_distance(pareto[j]) 
            pareto[j].sort(key=lambda distance: distance, reverse=False) 
            
            #newPopulation.extend(pareto[j])

            returned_pareto = pareto
            population = newPopulation

            pareto = self.genetic.fast_non_dominated_sort(population)
            distance = [0] * len(pareto)
            for p in range(len(pareto)):
               distance[p] = self.genetic.crowding_distance(pareto[p])
            
            """CREATION OF A CHILD"""
            child = self.genetic.create_child(population)
            """END"""            
        
        return returned_pareto
    

    def evolveDNSGAIIA(self, population:list, n_solutions):
        self.genetic.evaluate_objective_values(population,self.n_individuals)
        pareto = self.genetic.fast_non_dominated_sort(population)
        
        distance = []
        for i in range(len(pareto)):
            distance.append(self.genetic.crowding_distance(pareto[i]))
        
        """CREATION OF A CHILD"""
        child = self.genetic.create_child(population)
        """END"""

                
        for i in tqdm (range (self.n_generations)):
            
            # Fast Changing environment
            if i%10 == 0:
                print('Hello')
                temp_population = self.genetic.generate_random_solutions(n_solutions)
                obj = self.genetic.calculate_objective_values(temp_population, n_solutions)
                population = self.genetic.replace_element(population, obj, n_solutions)


            population.extend(child)            
            pareto = self.genetic.fast_non_dominated_sort(population)
            
            newPopulation = []


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
            
            """CREATION OF A CHILD"""
            child = self.genetic.create_child(population)
            """END"""            
        
        return returned_pareto

        
    def evolveCOEA(self, population):
        self.genetic.cooperative_competitive(population, 10)

