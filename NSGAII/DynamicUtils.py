import random

class DynamicUtils:

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

		#if ((pop1[i] > pop1[j] and pop2[i] > pop2[j]) or (pop1[i] >= pop1[j] and pop2[i] > pop2[j]) or (pop1[i] > pop1[j] and pop2[i] >= pop2[j])):		
		return (True and pop1 <= pop2) and (False or pop1 < pop2)

	# Generation of random population used for dynamic optimisation
    
	def generate_random_solutions(self):
		"""TODO: add documentation """
		solutions = []
		
		for i in range(self.n_individuals):
			temp = []
			for j in range(self.n_variables):
				#variable_values = round(random.uniform(min, max),2)
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


	def fast_non_dominated_sort(self, population):
		dominated_solutions = [0] * len(population)	# Dominated solutions S
		count = [0] * len(population)	# domination counter n

		pareto_front = [[]]
		pareto_front_obj = [[]]
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
			store_temp_fronts_obj = []		# representing Q
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


	def check_layers(self, front):
		newPopulation = []
		
		for i in range(len(front)):
			if front[i][0] + len(newPopulation) <= self.n_individuals:
				#newPopulation.append(front[i][0])
				print('Hello')
			else:
				print('Here')
				self.crowding_distance(front)
				break
		
		return newPopulation


	def crowding_distance(self, pareto_front):
		if len(pareto_front) > 0:
			l = len(pareto_front)
			distance = [0] * l

			for j in range(l):
				pareto_front.sort()

				distance[0] = distance[l-1] = 123456789

				for i in range(1,l-1):
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

		# child1 = []
		# child2 = []

		# for i in range(2):
		# 	#print(parent1[i], parent2[i])
		# 	u = random.random()
		# 	if u <= 0.5:
		# 		beta = (2 * u) ** (1/(n_c + 1))
		# 	else:
		# 		beta = (1/(2 * (1 - u))) ** (1/(n_c + 1))

		# 	child1.append(0.5 * ((1 + beta) * parent1[i] + (1 - beta) * parent2[i]))
		# 	child2.append(0.5 * ((1 - beta) * parent1[i] + (1 + beta) * parent2[i]))

		
		# return [child1, child2]


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


	def get_fitness(self):
		return self.n_generations 
	
	def split_populations(self, population):
		list1 = []
		list2 = []
		size = len(population)//2
		list1.append(population[:size])
		list2.append(population[size:len(population)])
		
		return list1, list2
	
	def split_populations(self, population, n):
		return list(population[i::n] for i in range(n))
	
	def cooperative_process(self, population, n):	
		# Implementation of the cooperative process
		# Binary Tournament 
		# get the result from the Binary Tournament --> Crossover --> Mutation

		Si = population[0]
		combined_solution= []
		archive = []

		for j in range(len(Si)):
			combined_solution.append(Si[j])
			for i in range(1, n):
				combined_solution.append(population[i][j])

			"""TODO: Evaluate the solution"""
			"""TODO: Update archive"""

		
		for j in range(len(Si)):
			"""TODO: Pareto Rank"""
			"""TODO: Calculate Niche count"""


		"""TODO: Update Si"""
		return Si



	# Implementation of the competitive process
	def competitive_process(self, population, n):
		# Shuffle population --> Crossover --> Mutation

		# Define the competition pool as an empty list
		competition_pool = []

		for i in range(n):
			# Insert the representative of the subpopulation in the competition pool. In this case the representative is the first element of each subpopulation
			competition_pool.append(population[i][0])

			if n > len(population[i]):
				r = random.randint(0,n)
				competition_pool.extend(population[r])
			elif n <= len(population[i]):
				r = random.randint(0,n)
				competition_pool.extend(population[r])
				elem = random.choice(population[i])
				print(elem)
				competition_pool.append(elem)
			
			self.cooperative_process()
			"""TODO: need to implement the winning subpopulation Sk"""
			"""TODO:  Si = Sk """

	def cooperative_competitive(self, population, n):

		# Split the population in n parts using the method
		subpopulations = self.split_populations(population, n)

		# Get the fitness value
		n_fitness = self.get_fitness()
	
		for i in range(self.n_generations):
			if i >= n_fitness:
				self.cooperative_process()
				"""TODO: Update and Return Archive"""
			else:
				r = random.randint(0,1)
				if r == 0:
					newPopulation = self.cooperative_process()
					"""CALL: Binary Tournament"""
					"""CALL: CROSSOVER"""
					"""CALL: MUTATION"""
				else:
					self.competitive_process(subpopulations, n)
					"""TODO: Shuffle subpopulation individuals"""
					"""CALL: CROSSOVER"""
					"""CALL: MUTATION"""


	# The tournment selection implemented takes as input a list and determines the dominant among the others
	def tournament_selection(self, population):			
		tournament_size = self.n_variables	# randomly chosen
		tournament = []
		best_individual = []

		""" 
		Tournament selection takes five random individuals from the population and returns the best
		"""
		for i in range(2):
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