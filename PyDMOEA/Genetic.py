import random

class Genetic:
    def __init__(self, n_individuals, n_generations, n_variables, min, max):
        """ Helper class to perform the genetic operations used in NSGAII and COEA with their relative dynamic variants

        Parameters
        ----------
        n_individuals : int
            Number of individuals of a population
        n_generations : int
            Number of iterations performed by the algorithm
        n_variables : int
            Number of variables defined by the specifications of the problem
        min : int
            Minimum value generated by the functions
        max : int 
            Maximum value generated by the functions
        """
        self.n_individuals = n_individuals
        self.n_generations = n_generations
        self.n_variables = n_variables
        self.min = min
        self.max = max
        
	
   
    def isDominated(self, pop1, pop2):
        """Helper function to determine which population is dominant

        Parameters
        ----------
        pop1 : list
            List of individuals
        pop2 : list
            List of individuals

        Returns
        -------
        Boolean
            Dominant population is returned
        """

        return (True and pop1 <= pop2) and (False or pop1 < pop2)

    def generate_random_solutions(self, n):
        """ Generation of random population used for static and dynamic optimisation

        Parameters
        ----------
        n : int
            number of individuals generated

        Returns
        -------
        list
            list of individuals (population)
        """
        solutions = []
        
        for i in range(n):
            temp = []
            for j in range(self.n_variables):
                variable_values = random.uniform(self.min, self.max)
                temp.append(variable_values)
            solutions.append(temp)

        return solutions
     

    def get_best(self, population):
        """ Helper function to determine the best individual

        Parameters
        ----------
        population : list
            List of individuals

        Returns
        -------
        list
            Best individual according to the parameters
        """
        # First element is temporary the best
        best = population[0]
        
        for i in range(1,len(population)):
            if population[i] > best:
                best = population[i]

        # Return the best value
        return best

    def sbx(self, parent1, parent2, n_c):
        """ Simulated Binary Crossver function

        Code adapted from: https://github.com/DEAP/deap/blob/master/deap/tools/crossover.py

        Parameters
        ----------
        parent1 : list
            List of 2 elements containing the x,y generated by the objective function
        parent2 : list
            List of 2 elements containing the x,y generated by the objective function
        n_c : int
            Distribution index used for the crossover operation

        Returns
        -------
        list
            List of 2 individuals generated
        """
        for i, (x1, x2) in enumerate(zip(parent1, parent2)):
            # Determine a random u value between 0 to 1
            u = random.random()
            # Calculate beta
            if u <= 0.5:
                beta = (2 * u) ** (1/(n_c + 1))
            else:
                beta = (1/(2 * (1 - u))) ** (1/(n_c + 1))

            # Create the new children
            parent1[i] = 0.5 * ((1 + beta) * x1 + (1 - beta) * x2)
            parent2[i] = 0.5 * ((1 - beta) * x1 + (1 + beta) * x2)

        return [parent1, parent2]




    def polynomial_mutation(self, population, eta):
        """ Polynomial mutation for the selected solutions

        Parameters
        ----------
        population : list
            List of individuals
        eta : int
            Mutation Probability index

        Returns
        -------
        list
            List of individuals mutated
        """

        xmin = 0    # Lower boundary for mutation
        xmax = 1    # Upper boundary for mutation
        for i in range(len(population)):
            x = population[i]
            # Generate a random number between 0 to 1
            u = random.random()
            # Calculate delta
            if u <= 0.5:
                delta = (2 * u) ** ((1 / (eta + 1))) - 1	
                delta_x = xmin - x			
            else:
                delta = 1 - (2 * (1 - u)) ** (1 / (eta + 1))
                delta_x = xmax - x

            # Create the mutated solutions
            x_ = x + delta_x * delta

            population[i] = x_

        # Return the new solutions
        return population
    
