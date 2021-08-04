import numpy

from ga_component.fitness_function import fitness_function
from model.data_types import Chromosome


def __fitness_proportionate_selection(population: list[Chromosome], fitness_scores: list[int], max_pop_size: int) \
        -> list[Chromosome]:
    """
    Fitness proportionate selection without replacement
    """
    sum_all_fitness = sum(fitness_scores)
    # Normalise fitness among the population
    selection_prob = [fitness_score / sum_all_fitness for fitness_score in fitness_scores]

    # Since numpy.random.choice() works on 1-D flat lists, lets map out the indices of population into population_idx
    population_idx = [i for i in range(len(population))]

    # Randomly select upto 'max_pop_size' chromosomes, with selection probability 'selection_prob'
    # replace=False denotes that selected chromosomes are not returned back to the selection pool again
    # In other words, all selections are unique
    selections = numpy.random.choice(population_idx, size=max_pop_size, p=selection_prob, replace=False)

    # Remap population_idx to population list and return
    return [population[idx] for idx in selections]  # pruned population


def __simple_sort_selection(population: list[Chromosome], fitness_scores: list[int], max_pop_size: int) \
        -> list[Chromosome]:
    """
    Simple sort selection - selects the top 'max_pop_size' sorted by fitness_scores in descending order
    """
    # Since population can be a mix of numpy arrays and normal lists - we will use indexes to map 1-1
    population_idx = [i for i in range(len(population))]
    joined_list = zip(fitness_scores, population_idx)
    sorted_joined_list = sorted(joined_list, reverse=True)
    sorted_population_idx = [chromosome for _, chromosome in sorted_joined_list]
    sorted_population = []
    for idx in sorted_population_idx:
        sorted_population.append(population[idx])
    return sorted_population[:max_pop_size]  # pruned population


def __populate_fitness_scores(population: list[Chromosome], min_fitness_score: int, max_fitness_score: int) \
        -> tuple[list[int], Chromosome]:
    fitness_scores = []
    solution = None  # in case we find a chromosome with max_fitness_score while populating fitness_scores
    for chromosome in population:
        score = fitness_function(chromosome, min_fitness_score)
        if score >= max_fitness_score:  # Solution found!
            solution = chromosome
            if score > max_fitness_score:
                print("Warning! Found fitness score: " + str(score) + " more than max: " +
                      str(max_fitness_score) + ". Please check your values\n")
            break
        fitness_scores.append(score)
    return fitness_scores, solution


def selection(population: list[Chromosome], min_fitness_score: int, max_fitness_score: int, max_pop_size: int,
              strategy: str) -> tuple[list[Chromosome], Chromosome]:
    """
    :param population: List of chromosomes to perform the selection on.
    :param min_fitness_score: Used for fitness_function biasing the minimum score (for example +1).
    :param max_fitness_score: Used during selection as an "abort" criteria. If the best solution is found, the program
                              ceases to continue
    :param max_pop_size: The size of selected candidates
    :param strategy: fitness_proportionate_selection or simple_sort_selection
    :return: A tuple of 2 items - pruned population and (if found) the chromosome having max_fitness_score
    """
    # fitness_scores is a list which maps 'fitness_score' with 'population' list 1 to 1
    # this list helps act as a comparator during selection_strategy
    # While populating fitness scores, we will also check if a solution is found - as an algorithm optimisation
    fitness_scores, solution = __populate_fitness_scores(population, min_fitness_score, max_fitness_score)

    if solution is not None:
        return population, solution

    if strategy == 'simple_sort':
        return __simple_sort_selection(population, fitness_scores, max_pop_size), solution
    else:
        # Default selection strategy
        return __fitness_proportionate_selection(population, fitness_scores, max_pop_size), solution
