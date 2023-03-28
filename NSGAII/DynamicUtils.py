import random
import numpy as np

class DynamicUtils:

	def __init__(self, problem, n_individuals=100, n_generations=10):
		self.problem = problem
		self.n_individuals = n_individuals
		self.n_generations = n_generations
		self.objective_values = []

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
		

	
	def dominates(self, other_individual):
		and_condition = True
		or_condition = False
		for first, second in zip(self.objectives, other_individual.objectives):
			and_condition = and_condition and first <= second
			or_condition = or_condition or first < second
		return (and_condition and or_condition)

		

	# Generation of random population used for dynamic optimisation
    
	def generate_random_solutions(self, min, max, n_variables):
		"""TODO: add documentation """
		solutions = []
		
		for i in range(self.n_individuals):
			temp = []
			for j in range(n_variables):
				variable_values = round(random.uniform(min, max),2)
				temp.append(variable_values)
			solutions.append(temp)

		return solutions
	
	def init_population(self, population):
		for i in range(self.n_individuals):			
			f1, f2 = self.problem.evaluate_objective_values(population[i])
			temp = [f1, f2]
			self.objective_values.append(temp)
		return self.objective_values


	def fast_non_dominated_sort(self, population):
		dominated_solutions = [0] * len(population)	# Dominated solutions S
		count = [0] * len(population)	# domination counter n

		pareto_front = [[]]
		rank = [0] * len(population)

		for p in range(len(population)-1):
			dominated_solutions[p] = []
			count[p] = 0

			for q in range(len(population)-1):
				if self.isDominated(self.objective_values[p], self.objective_values[p+1]):
					dominated_solutions[p].append(self.objective_values[q])
				else:
					count[p] = count[p] + 1
			if count[p] == 0:				
				rank[p] = 0     
				pareto_front.append(self.objective_values[p])

		
		i = 1
		print(pareto_front)
		print('\n\n')
		print(dominated_solutions)

		print('\n\n')


		while len(pareto_front[i]) > 0:
			store_temp_fronts = []		# representing Q
			for p in range(len(pareto_front[i])):
				for q in range(len(dominated_solutions[p])):
					count[q] = count[q] - 1 
					if count[q] == 0:
						rank[q] = i + 1
						store_temp_fronts.append(self.objective_values[q])
			i = i + 1
			pareto_front.append(store_temp_fronts)

		
		del pareto_front[0]
		return pareto_front
			

	def check_layers(self, front):
		print(front)
		print(len(front))
		print(front[0][0])
		print(front[1][0])
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
					distance[i] = distance[i]+ (pareto_front[i+1] - pareto_front[i-1])/(max(pareto_front)-min(pareto_front))


			return distance

	
	#n_c is the distribution index
	def sbx(self, parent1, parent2, n_c):
		# http://doi.acm.org/10.1145/1276958.1277190



		for i, (x1, x2) in enumerate(zip(parent1, parent2)):
			u = random.random()
			if u <= 0.5:
				beta = (2 * u) ** (1/(n_c + 1))
			else:
				beta = (1/(2 * (1 - u))) ** (1/(n_c + 1))

				
			parent1 = 0.5 * ((1 + beta) * x1 + (1 - beta) * x2)
			parent2 = 0.5 * ((1 - beta) * x1 + (1 + beta) * x2)
			#child1.append(c1)
			#child2.append(c2)

			child = [parent1, parent2]

		return child


	def polynomial_mutation(self, population, n_mutation):
		# https://www.sciencedirect.com/science/article/abs/pii/S0020025515007276

		for i in range(len(population)):
			u = random.random()
			if u <= 0.5:
				delta = (2 * u) ** ((1 / (n_mutation + 1))) - 1				
			else:
				delta = 1 - (2 * (1 - u)) ** (1 / (n_mutation + 1))

			x = population[i]
			xmin = 0
			xmax = 1
			delta_x = max(xmin - x, x - xmax)
			population[i] = x + delta_x * delta

		return population


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
		tournament_size = 2	# randomly chosen
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