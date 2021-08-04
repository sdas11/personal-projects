from ga_component.fitness_function import fitness_function
from model.data_types import EmptyGene

if __name__ == '__main__':
    MIN_FITNESS_SCORE = 1
    # Example 1
    fitness_score = fitness_function(
        [
            ['R', 'D', 'O', 'W'],
            ['O', 'W', 'R', 'D'],
            ['D', 'R', 'W', 'O'],
            ['W', 'O', 'D', 'R']
        ],
        MIN_FITNESS_SCORE
    )
    print("The fitness score is: " + str(fitness_score) + ". It should be 12")

    # Example 2
    fitness_score = fitness_function(
        [
            ['W', 'O', 'R', 'D'],
            ['W', 'O', 'R', 'D'],
            ['W', 'O', 'R', 'D'],
            ['W', 'O', 'R', 'D']
        ],
        MIN_FITNESS_SCORE
    )
    print("The fitness score is: " + str(fitness_score) + ". It should be 4")

    # Example 3
    fitness_score = fitness_function(
        [
            ['W', 'W', 'R', 'D'],
            ['W', 'W', 'R', 'D'],
            ['W', 'W', 'R', 'D'],
            ['W', 'W', 'R', 'D']
        ],
        MIN_FITNESS_SCORE
    )
    print("The fitness score is: " + str(fitness_score) + ". It should be 0")

    # Example 4
    fitness_score = fitness_function(
        [[EmptyGene for i in range(4)] for j in range(4)],
        MIN_FITNESS_SCORE
    )
    print("The fitness score is: " + str(fitness_score) + ". It should be 0")
