import random

class NSGAUtils:

	def __init__(self, problem, n_individuals, n_generations, n_variables, min, max):
		self.problem = problem
		self.n_individuals = n_individuals
		self.n_generations = n_generations
		self.n_variables = n_variables
		self.objective_values = []
		self.min = min
		self.max = max

	# Helper function to check if the element in the list
	def check_list(self, list):    	
		return all(x == list[0] for x in list)

	# Helper function to sort values of a list by index
	def sort_by_index(self, list):
		sorted_list = []
		while self.check_list(list) == False:
			index = list.index(min(list))
			sorted_list.append(index)
			list[index] = 123456      #random big number

		return sorted_list

	
	def isDominated(self, pop1, pop2):
		"""Helper function to check if pop1 dominates pop2

		https://oklahomaanalytics.com/data-science-techniques/nsga-ii-explained/
		
		Parameters
		----------
		pop1: list
		pop2: list
		"""

		return (True and pop1 <= pop2) and (False or pop1 < pop2)

	# Generation of random population used for dynamic optimisation
	def generate_random_solutions(self, n):
		"""TODO: add documentation """
		solutions = []
		
		for i in range(n):
			temp = []
			for j in range(self.n_variables):
				variable_values = random.uniform(self.min, self.max)
				temp.append(variable_values)
			solutions.append(temp)

		return solutions
	
	def evaluate_objective_values(self, population, n):
		for i in range(n):		
			f1, f2 = self.problem.evaluate_objective_values(population[i])
			temp = [f1, f2]
			self.objective_values.append(temp)
		return self.objective_values
	

	def calculate_objective_values(self, population, n):
		temp_obj = []
		for i in range(n):		
			f1, f2 = self.problem.evaluate_objective_values(population[i])
			temp_obj.append([f1,f2])
		return temp_obj
	

	def replace_element(self, population:list, new_element, n):
		
		j = 0
		for i in range(n):
			r = random.randrange(len(population))
			population.pop(r)
			population.append(new_element[j])
			j = j + 1

		return population


	def fast_non_dominated_sort(self, population):
		dominated_solutions = [0] * len(population)	# Dominated solutions S
		count = [0] * len(population)	# domination counter n

		pareto_front = [[]]
		rank = [0] * len(population)


		for p in range(len(population)):
			dominated_solutions[p] = []
			count[p] = 0

			for q in range(p+1, len(population)):
				if self.isDominated(self.objective_values[p], self.objective_values[q]):
					if self.objective_values[q] not in dominated_solutions[p]:
						dominated_solutions[p].append(self.objective_values[q])
				elif self.isDominated(self.objective_values[q], self.objective_values[p]):
					count[p] = count[p] + 1
			if count[p] == 0:				
				rank[p] = 0     
				pareto_front[0].append(self.objective_values[p])

		i = 0
		while len(pareto_front[i]) > 0:
			store_temp_fronts = []		# representing Q
			for p in range(len(pareto_front[i])):
				for q in range(0, len(dominated_solutions)):
					count[q] = count[q] - 1 
					if count[q] == 0:
						rank[q] = i + 1
						store_temp_fronts.append(self.objective_values[q])
			
			pareto_front.append(store_temp_fronts)
			i = i + 1

		return pareto_front

	def crowding_distance(self, pareto_front):
		if len(pareto_front) > 0:
			
			distance = [0 for i in range(0,len(pareto_front))]

			for j in range(len(pareto_front)):
				pareto_front[j].sort()
				distance[0] = 123456789
				distance[len(pareto_front)-1] = 123456789

				for i in range(1,len(pareto_front)-1):
					distance[i] = distance[i]+ (pareto_front[i+1][0] - pareto_front[i-1][0])/(max(pareto_front[i])-min(pareto_front[i]))

			return distance

	
	#n_c is the distribution index
	def sbx(self, parent1, parent2, n_c):
		# http://doi.acm.org/10.1145/1276958.1277190
		"""
		A large value of ηc gives a higher probability for creating ‘near-parent’ 
		solutions (thereby allowing a focussed search) and a small value of ηc allows 
		distant solutions to be selected as offspring (thereby allowing to make diverse search).
		"""

		for i, (x1, x2) in enumerate(zip(parent1, parent2)):
			u = random.random()
			if u <= 0.5:
				beta = (2 * u) ** (1/(n_c + 1))
			else:
				beta = (1/(2 * (1 - u))) ** (1/(n_c + 1))


			parent1[i] = 0.5 * ((1 + beta) * x1 + (1 - beta) * x2)
			parent2[i] = 0.5 * ((1 - beta) * x1 + (1 + beta) * x2)

		return [parent1, parent2]
	

	def polynomial_mutation(self, population, eta):
		# https://www.sciencedirect.com/science/article/abs/pii/S0020025515007276

		# Add a for loop for iterating each variable and add probability check
		
		xmin = 0
		xmax = 1
		for i in range(len(population)):
			x = population[i]
			u = random.random()
			if u <= 0.5:
				delta = (2 * u) ** ((1 / (eta + 1))) - 1	
				delta_x = xmin - x			
			else:
				delta = 1 - (2 * (1 - u)) ** (1 / (eta + 1))
				delta_x = xmax - x

			x_ = x + delta_x * delta

			population[i] = x_

		return population
	

	def create_child(self, population):
		child = []
		
		while len(child) < len(population):
			parent1 = self.tournament_selection(population)
			parent2 = parent1

			while parent1 == parent2:
				parent2 = self.tournament_selection(population)
					
			temp_child = self.sbx(parent1[0], parent2[0], 200)
			#temp_child[0] = self.genetic.polynomial_mutation(temp_child[0], 20, 1/self.n_variables)
			#temp_child[1] =self.genetic.polynomial_mutation(temp_child[1], 20, 1/self.n_variables)
			temp_child[0] = self.polynomial_mutation(temp_child[0], 200)
			temp_child[1] = self.polynomial_mutation(temp_child[1], 200)


			# Init population + append children objectives to population objectives
			self.evaluate_objective_values(temp_child,2)

			child.append(temp_child)
		
		return child
	
	# The tournment selection implemented takes as input a list and determines the dominant among the others
	def tournament_selection(self, population):			
		tournament_size = self.n_variables	# randomly chosen
		tournament = []
		best_individual = []

		""" 
		Tournament selection takes five random individuals from the population and returns the best
		"""
		for i in range(3):
			for j in range(tournament_size):
				r = random.choice(population)
				tournament.append(r)

			best_individual.append(self.get_best(tournament))
			tournament = []
		
		return best_individual
	

	def get_best(self, population):
		best = population[0]

		for i in range(1,len(population)):
			if population[i] > best:
				best = population[i]

		return best

###################################################################################################


class COEAUtils:

	def __init__(self, problem, n_individuals, n_generations, n_variables, min, max):
		self.problem = problem
		self.n_individuals = n_individuals
		self.n_generations = n_generations
		self.n_variables = n_variables
		self.objective_values = []
		self.min = min
		self.max = max
		self.archive = []

	# Generation of random population used for dynamic optimisation
	def generate_random_solutions(self, n):
		"""TODO: add documentation """
		solutions = []
		
		for i in range(n):
			temp = []
			for j in range(self.n_variables):
				variable_values = random.uniform(self.min, self.max)
				temp.append(variable_values)
			solutions.append(temp)

		return solutions
	
	def evaluate_objective_values(self, population, n):
		for i in range(n):		
			f1, f2 = self.problem.evaluate_objective_values(population[i])
			temp = [f1, f2]
			self.objective_values.append(temp)
		return self.objective_values
	

	# The tournment selection implemented takes as input a list and determines the dominant among the others
	# Edited compared to NSGAII
	def tournament_selection(self, population):			
		tournament_size = 5	# randomly chosen
		tournament = []
		best_individual = []

		""" 
		Tournament selection takes two random individuals from the population and returns the best
		"""
		for j in range(tournament_size):
			r = random.choice(population)
			tournament.append(r)
		
		best_individual.append(self.get_best(tournament))

		return best_individual
	

	def get_best(self, population):
		best = population[0]
		
		for i in range(1,len(population)):
			if population[i] > best:
				best = population[i]

		return best
	

	#n_c is the distribution index
	def sbx(self, parent1, parent2, n_c):
		# http://doi.acm.org/10.1145/1276958.1277190
		"""
		A large value of ηc gives a higher probability for creating ‘near-parent’ 
		solutions (thereby allowing a focussed search) and a small value of ηc allows 
		distant solutions to be selected as offspring (thereby allowing to make diverse search).
		"""

		for i, (x1, x2) in enumerate(zip(parent1, parent2)):
			u = random.random()
			if u <= 0.5:
				beta = (2 * u) ** (1/(n_c + 1))
			else:
				beta = (1/(2 * (1 - u))) ** (1/(n_c + 1))


			parent1[i] = 0.5 * ((1 + beta) * x1 + (1 - beta) * x2)
			parent2[i] = 0.5 * ((1 - beta) * x1 + (1 + beta) * x2)

		return [parent1, parent2]
	

	def polynomial_mutation(self, population, eta):
		# https://www.sciencedirect.com/science/article/abs/pii/S0020025515007276

		# Add a for loop for iterating each variable and add probability check
		
		xmin = 0
		xmax = 1
		for i in range(len(population)):
			x = population[i]
			u = random.random()
			if u <= 0.5:
				delta = (2 * u) ** ((1 / (eta + 1))) - 1	
				delta_x = xmin - x			
			else:
				delta = 1 - (2 * (1 - u)) ** (1 / (eta + 1))
				delta_x = xmax - x

			x_ = x + delta_x * delta

			population[i] = x_

		return population
	
	def create_child(self, population):
		
		parent1 = self.tournament_selection(population)
		parent2 = parent1

		while parent1 == parent2:
			parent2 = self.tournament_selection(population)
		
				
		temp_child = self.sbx(parent1[0], parent2[0], 1)
		#temp_child[0] = self.genetic.polynomial_mutation(temp_child[0], 20, 1/self.n_variables)
		#temp_child[1] =self.genetic.polynomial_mutation(temp_child[1], 20, 1/self.n_variables)
		temp_child[0] = self.polynomial_mutation(temp_child[0], 1)
		temp_child[1] = self.polynomial_mutation(temp_child[1], 1)


		# Init population + append children objectives to population objectives
		self.evaluate_objective_values(temp_child,2)
	
		
		return temp_child


	def get_fitness(self):
		return self.n_generations 
	
	
	def split_populations(self, population, n):
		return list(population[i::n] for i in range(n))
	

	def cooperative_competitive(self, population, n):	
		# Split the population in n parts using the method
		subpopulations = self.split_populations(population, n)

		print(subpopulations, '\n')

		# Get the fitness value
		n_fitness = self.get_fitness()

		newPopulation = []
	
		for i in range(n_fitness):
			if len(newPopulation) < self.n_individuals:
				r = random.randint(0,1)
				if r == 0 or i % 10 == 0:
					newPopulation.extend(self.competitive_process(subpopulations))
					# Shuffle subpopulation individuals"""
					random.shuffle(newPopulation)
					# """CALL: CROSSOVER"""
					# """CALL: MUTATION"""
					child = self.create_child(newPopulation)
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
		


	def cooperative_process(self, population):	
		combined_solution = []

		index = random.randint(0, self.n_variables)
		for i in range(len(population)):
			combined_solution.append(population[i][index])
		
		self.evaluate_objective_values(combined_solution, 2)

		self.archive.extend(combined_solution)
		
		#for j in range(len(Si)):
			#"""TODO: Pareto Rank"""
			#"""TODO: Calculate Niche count"""


		#Return Archive
		return self.archive


	# Implementation of the competitive process
	def competitive_process(self, population:list):
		# Shuffle population --> Crossover --> Mutation

		# Define the competition pool as an empty list
		competition_pool = []
		n = len(population)

		for i in range(len(population)):
			# Insert the representative of the subpopulation in the competition pool. In this case the representative is a random index
			index = random.randint(0, self.n_variables)
			competition_pool.append(population[i][index])
			

			if n > len(population[i]):
				index = random.randint(0, self.n_variables)
				competition_pool.extend(population[i][index])
			elif n <= len(population[i]):
				elem = random.choice(population)
				index = random.randint(0, self.n_variables)
				competition_pool.extend([elem[index]])

			"""TODO: call cooperative process"""
			"""TODO: need to implement the winning subpopulation Sk"""
			"""TODO:  Si = Sk """

		return competition_pool


###################################################################################################

class MOEADUtils:

	def __init__(self, problem, n_individuals, n_generations, n_variables, min, max):
		self.problem = problem
		self.n_individuals = n_individuals
		self.n_generations = n_generations
		self.n_variables = n_variables
		self.objective_values = []
		self.min = min
		self.max = max

	# Generation of random population used for dynamic optimisation
	def generate_random_solutions(self, n):
		"""TODO: add documentation """
		solutions = []
		
		for i in range(n):
			temp = []
			for j in range(self.n_variables):
				variable_values = random.uniform(self.min, self.max)
				temp.append(variable_values)
			solutions.append(temp)

		return solutions
	
	def evaluate_objective_values(self, population, n):
		for i in range(n):		
			f1, f2 = self.problem.evaluate_objective_values(population[i])
			temp = [f1, f2]
			self.objective_values.append(temp)
		return self.objective_values

	def initilizeMOEAD(self, population):
		self.objective_values = self.evaluate_objective_values(population, self.n_individuals)
		print(self.objective_values)


