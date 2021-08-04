# allowed_alleles denotes the sample space of gene variants
# For our 4x4 Word-Sudoku puzzle, we define 4 alleles as: ['W', 'O', 'R', 'D']
# Ideally this should be a Python set - however some operations like selecting
# random allele from the set is inefficient
allowed_alleles = ['W', 'O', 'R', 'D']

EmptyGene = '_'

# A set of Genes(str) is called a chromosome. Each chromosome represents a candidate solution to the problem
# Chromosome is composed of elements from the allowed_alleles
# For our 4x4 Word-Sudoku puzzle, we represent the 4 x 4 grid as a Chromosome of type SquareMatrix
# Expected rows = cols
Chromosome = list[list[str]]

# Preserve Arrangement Matrix
BooleanMatrix = list[list[bool]]

# Constraints for GA solver
SolverProperties = {
    'min_fitness_score': int,
    'max_fitness_score': int,
    'max_population': int,
    'selection_strategy': str,
    'num_of_crossovers_per_generation': int,
    'mutation_probability': float
}