import copy
import numpy
import random
import time

from ga_component.ga_solver import __read_properties, __get_highest_ranked_chromosome
from ga_component.mutation import flip_mutation
from ga_component.row_column_crossover import crossover
from ga_component.selection import selection
from model.data_types import Chromosome, BooleanMatrix, allowed_alleles, SolverProperties

'''
!!!!!!!                 !!!!!!!                !!!!!!!
THIS FILE IS A COPY OF ga_solver.py WITH DEBUG STATEMENTS ADDED. SINCE DEBUG STATEMENTS MAKE THE CODE CLUTTERED
PLEASE REFER TO ga_solver.py for UNDERSTANDING THE CODE AND THE DOCUMENTATION
'''


def ga_grid_solver_debug(
        population: list[Chromosome],
        preserve_arrangement: BooleanMatrix,
        solver_properties: SolverProperties,
        max_iterations: int,
        debug_data: dict) -> tuple[Chromosome, bool, int, float]:
    """
        !!!!!!!                 !!!!!!!                !!!!!!!
        THIS FILE IS A COPY OF ga_solver.py WITH DEBUG STATEMENTS ADDED. SINCE DEBUG STATEMENTS MAKE THE CODE CLUTTERED
        PLEASE REFER TO ga_solver.py for UNDERSTANDING THE CODE AND THE DOCUMENTATION
    """

    # To time the run
    start_time = time.process_time()

    # Read properties
    min_fitness_score, max_fitness_score, max_population, \
        selection_strategy, crossover_per_iter, mutation_prob_per_chromosome = __read_properties(solver_properties)

    # Initialise vars
    solution = None
    is_solution_found = False
    iterations = 0

    # Initially set this to True to allow Selection (as Selection is the first step)
    # These two vars are used to check whether we should do a Selection or not.
    # For example, when no mutation or crossover has happened, we should skip selection
    # Mutation happening is affected by mutation_prob_per_chromosome
    # Crossover happening depends on whether 2 distinct parents (chromosomes) are chosen (from random parent selection)
    crossovers_happened, mutations_happened = (True, True)

    # Debug Addition
    debug_data['seed_population'] = copy.deepcopy(population)
    debug_data['debug_iterations'] = []
    debug_list = debug_data['debug_iterations']

    # Run GA (order of operations -> selection, crossover, mutation)
    while iterations < max_iterations:
        # Selection (prunes the population to max_population require)
        if crossovers_happened or mutations_happened:
            # Also returns non-None value for 'solution' if  a chromosome with max_fitness_score is found
            population, solution = selection(population, min_fitness_score, max_fitness_score, max_population,
                                             selection_strategy)

        # After selection phase, check if a solution is already found
        if solution is not None:
            is_solution_found = True
            break
        # Debug Addition # Debug Addition
        else:
            __set_debug_info(iterations, "selection_happened", debug_list, crossovers_happened or mutations_happened)
            if crossovers_happened or mutations_happened:
                __set_debug_info(iterations, "population_after_selection", debug_list, copy.deepcopy(population))

        # Reset the flags back to False
        crossovers_happened, mutations_happened = (False, False)

        # Crossover
        # Appends the crossover children to the population list directly
        crossovers_happened = __select_parents_and_crossover(crossover_per_iter, population, iterations, debug_list)

        # Debug Addition
        __set_debug_info(iterations, "population_after_crossover", debug_list, copy.deepcopy(population))
        mutation_data = []
        idx = 0

        # Mutation
        for chromosome in population:
            mutation_happened, row_idx, col_idx = flip_mutation(chromosome, preserve_arrangement, allowed_alleles,
                                                                mutation_prob_per_chromosome)
            mutations_happened = mutation_happened or mutations_happened

            # Debug Addition
            if mutation_happened:
                mutation_data.append({
                    "population_idx": idx,
                    "flip_row_idx": row_idx,
                    "flip_col_idx": col_idx
                })
            idx = idx + 1

        # Debug Addition
        __set_debug_info(iterations, "mutation", debug_list, copy.deepcopy(mutation_data))
        __set_debug_info(iterations, "population_after_mutation", debug_list, copy.deepcopy(population))

        iterations = iterations + 1

    # We reach here when either a solution is found or max iteration criteria has been met
    if solution is None:
        # If no solution, we try to return the most optimal answer (max fitness score) from the current population
        solution = __get_highest_ranked_chromosome(population, min_fitness_score)

    end_time = time.process_time()

    return solution, is_solution_found, iterations, end_time - start_time


def __set_debug_info(iteration: int, info_type: str, debug_container: list, debug_data):
    if debug_container is None:
        debug_container = []
    try:
        debug_container[iteration]
    except IndexError:
        debug_container.insert(iteration, {})

    debug_container[iteration][info_type] = debug_data


def __select_parents_and_crossover(max_crossovers: int, population: list[Chromosome], debug_iteration: int,
                                  debug_list: list) -> bool:
    # Debug Addition
    crossover_debug_data = []

    _crossover_happened = False
    crossover_iter = 0  # how many times we want to crossover (allow mating) per generation
    while crossover_iter < max_crossovers:

        # Select a pair of random parent chromosomes
        # Select indices explicitly for reporting (instead of directly selecting array element)
        random_parents_indices = random.sample(range(len(population)), 2)
        random_parents = [population[random_parents_indices[0]], population[random_parents_indices[1]]]
        # Skip crossover if parents are not different
        if numpy.array_equal(random_parents[0], random_parents[1]):
            crossover_iter = crossover_iter + 1
            # Debug Addition
            crossover_debug_data.insert(crossover_iter, {'crossover_done': False})
            continue
        else:
            _crossover_happened = True
            # Debug Addition
            crossover_debug_data.insert(crossover_iter, {'crossover_done': True})

        # Do the crossover
        row_swap_child, col_swap_child = crossover(random_parents[0], random_parents[1])

        # Debug Addition
        last_idx = len(population) - 1

        # Add it to existing population
        population.append(row_swap_child)
        population.append(col_swap_child)

        # Debug Addition
        crossover_debug_data[crossover_iter]["parent_id_1"] = random_parents_indices[0]
        crossover_debug_data[crossover_iter]["parent_id_2"] = random_parents_indices[1]
        crossover_debug_data[crossover_iter]["row_swap_child"] = copy.deepcopy(row_swap_child)
        crossover_debug_data[crossover_iter]["col_swap_child"] = copy.deepcopy(col_swap_child)
        crossover_debug_data[crossover_iter]["row_swap_child_id"] = last_idx + 1
        crossover_debug_data[crossover_iter]["col_swap_child_id"] = last_idx + 2

        crossover_iter = crossover_iter + 1

    # Debug Addition
    __set_debug_info(debug_iteration, "crossover", debug_list, crossover_debug_data)

    return _crossover_happened
