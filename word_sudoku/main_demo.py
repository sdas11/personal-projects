import numpy.random

from ga_component.fitness_function import fitness_function
from ga_component.ga_solver import ga_grid_solver
from model.data_types import allowed_alleles, Chromosome
from util.common import get_bool_matrix_for_filled_cells, ask_user_or_select_random_problem, populate_for_empty_genes

'''
    !!!!        !!!!
    MAIN PROGRAM, RUN THIS TO SEE THE DEMO
'''

solver_properties = {
    'min_fitness_score': 1,  # to prevent division errors we don't keep the min as 0 - bias by +1

    # 12 constraints - 4 rows, 4 cols, 4 subgrids - for every constraint satisfiability, +1 points are added
    'max_fitness_score': 12 + 1,  # 12 + min_fitness_score
    'max_population': 5,  # population size to send for next generation (after pruning during selection phase)
    'selection_strategy': 'fitness_proportionate_selection',  # fitness_proportionate_selection or simple_sort
    'num_of_crossovers_per_generation': 2,  # Note: Children per crossover after mating is fixed at 2
    'mutation_probability': 0.2  # Probability of genes (alleles) flipping for EACH individual in EACH iteration
}


def __get_problem_to_solve():
    _partial_chromosome = ask_user_or_select_random_problem()
    print("This is the input problem to solve")
    print(numpy.matrix(_partial_chromosome)), print("\n")
    return _partial_chromosome


def __get_seed_population_and_dont_modify_array(_partial_chromosome: Chromosome, _solver_properties):
    # Create a don't modify Boolean matrix to preserve original arrangement
    _dont_modify = get_bool_matrix_for_filled_cells(_partial_chromosome)

    # Seed an initial population of size 2 x population_size
    # All the populations have random alleles filled to complete the partial chromosome
    _seed_population = [populate_for_empty_genes(_partial_chromosome, allowed_alleles) for _ in
                        range(_solver_properties['max_population'] * 2)]

    return _seed_population, _dont_modify


'''
    !!!!        !!!!
    MAIN PROGRAM, RUN THIS TO SEE THE DEMO
'''
if __name__ == '__main__':
    partial_chromosome = __get_problem_to_solve()
    seed_population, dont_modify = __get_seed_population_and_dont_modify_array(partial_chromosome, solver_properties)

    # Run ga_grid_solver
    solution, solution_found, iterations, time_taken = ga_grid_solver(seed_population, dont_modify, solver_properties,
                                                                      max_iterations=20000)

    print("Solution") if solution_found else print("Sub Optimal Solution")
    print(numpy.matrix(solution))
    if not solution_found:
        print("Fitness Score: " + str(fitness_function(solution, solver_properties['min_fitness_score'])))
    print("\nTotal number of iterations: " + str(iterations))
    print("\nTime taken: " + str(time_taken) + " secs")
