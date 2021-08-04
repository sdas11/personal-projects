import numpy
import random
import time

from ga_component.fitness_function import fitness_function
from ga_component.mutation import flip_mutation
from ga_component.row_column_crossover import crossover
from ga_component.selection import selection
from model.data_types import Chromosome, BooleanMatrix, allowed_alleles, SolverProperties


def ga_grid_solver(
        population: list[Chromosome],
        preserve_arrangement: BooleanMatrix,
        solver_properties: SolverProperties,
        max_iterations: int) -> tuple[Chromosome, bool, int, float]:
    """
        This is the main function to solve a grid puzzle via genetic algorithm. Can solve for any "square" 2-D array
        (N rows and N cols) given an appropriate fitness function.

        Args:
            population: The problem we want to solve. Expected that Chromosome is a square 2-D array of characters.
            preserve_arrangement: Use this 2-D array to leave some cells untouched (no modification).
            solver_properties: Dictionary of solver properties. Check __read_properties for the property names.
            max_iterations: The maximum number of iterations GA can run for

        Returns:
            optimal_solution:  Solved (or partially solved in case of no solution / max_iteration exceeded)
            is_best_solution_found:  Boolean denoting if best solution was found (to avoid recheck by function caller)
            iterations_taken:  Number of iterations the solution was arrived at (or max_iteration if no solution)
            time_taken: Time taken in seconds
    """
    # To time the run
    start_time = time.process_time()

    # Read properties
    min_fitness_score, max_fitness_score, max_population, \
        selection_strategy, crossover_per_iter, mutation_prob_per_chromosome = __read_properties(solver_properties)

    # Initialise vars
    optimal_solution = None
    is_best_solution_found = False
    iterations = 0

    # Initially set this to True to allow Selection (as Selection is the first step)
    # This is done because we have a small optimisation check for Selection =>
    # These two vars are used to check whether we should do a Selection or not.
    # For example, when no mutation or crossover has happened, we should skip selection
    crossovers_happened, mutations_happened = (True, True)

    # Run GA (order of operations -> selection, crossover, mutation)
    while iterations < max_iterations:
        # Selection (prunes the population to max_population require)
        if crossovers_happened or mutations_happened:
            # Also returns non-None value for 'solution' if  a chromosome with max_fitness_score is found
            population, optimal_solution = selection(population, min_fitness_score, max_fitness_score, max_population,
                                                     selection_strategy)

        # After selection phase, check if a solution is already found
        if optimal_solution is not None:
            is_best_solution_found = True
            break

        # Reset the flags back to False
        crossovers_happened, mutations_happened = (False, False)

        # Crossover
        # Crossover happening depends on whether 2 distinct parents (chromosomes) are chosen
        # from random parent selection (for mating)
        # APPENDS the crossover children to the population list directly
        crossovers_happened = __select_parents_and_crossover(crossover_per_iter, population)

        # Mutation
        for chromosome in population:
            # Mutation happening is affected by mutation_prob_per_chromosome
            mutation_happened, row_idx, col_idx = flip_mutation(chromosome, preserve_arrangement, allowed_alleles,
                                                                mutation_prob_per_chromosome)
            mutations_happened = mutation_happened or mutations_happened

        iterations = iterations + 1

    # We reach here when either a solution is found or max iteration criteria has been met
    if optimal_solution is None:
        # If no solution, we try to return the most optimal answer (max fitness score) from the current population
        optimal_solution = __get_highest_ranked_chromosome(population, min_fitness_score)

    end_time = time.process_time()

    return optimal_solution, is_best_solution_found, iterations, end_time - start_time


def __read_properties(solver_properties: SolverProperties) -> tuple[int, int, int, str, int, float]:
    return solver_properties['min_fitness_score'], solver_properties['max_fitness_score'], \
           solver_properties['max_population'], solver_properties['selection_strategy'], \
           solver_properties['num_of_crossovers_per_generation'], solver_properties['mutation_probability']


def __get_highest_ranked_chromosome(population: list[Chromosome], min_fitness_score: int) -> Chromosome:
    fittest_chromosome = population[0]
    better_candidate_score = fitness_function(fittest_chromosome, min_fitness_score)
    for chromosome in population:
        temp_score = fitness_function(chromosome, min_fitness_score)
        if temp_score > better_candidate_score:
            fittest_chromosome = chromosome
            better_candidate_score = temp_score
    return fittest_chromosome


def __select_parents_and_crossover(max_crossovers: int, population: list[Chromosome]) -> bool:
    """
    This helper method selects the parents first - for the crossover operation.
    !! NOTE: This method mutates the population array - adds the children to it

    :return:
        _crossover_happened: Whether at-least 1 crossover happened or not
    """
    _crossover_happened = False
    crossover_iter = 0  # how many times we want to crossover (allow mating) per generation
    while crossover_iter < max_crossovers:

        # Select a pair of random parent chromosomes
        # Select list indices explicitly for reporting (instead of directly selecting array element)
        random_parents_indices = random.sample(range(len(population)), 2)
        random_parents = [population[random_parents_indices[0]], population[random_parents_indices[1]]]

        # Skip crossover if parents are not different
        if numpy.array_equal(random_parents[0], random_parents[1]):
            crossover_iter = crossover_iter + 1
            continue
        else:
            _crossover_happened = True

        # Do the crossover
        row_swap_child, col_swap_child = crossover(random_parents[0], random_parents[1])

        # Add it to existing population
        population.append(row_swap_child)
        population.append(col_swap_child)

        crossover_iter = crossover_iter + 1

    return _crossover_happened
