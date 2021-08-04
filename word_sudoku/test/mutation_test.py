import random

import numpy

from ga_component.mutation import flip_mutation
from model.data_types import allowed_alleles
from model.sample_problems import easy_problems
from util.common import get_bool_matrix_for_filled_cells

if __name__ == '__main__':
    sample_chromosome = random.choice(easy_problems)
    print("Selected sample chromosome")
    print(numpy.matrix(sample_chromosome))
    dont_flip = get_bool_matrix_for_filled_cells(sample_chromosome)
    print("Corresponding don't flip matrix")
    print(numpy.matrix(dont_flip))
    flip_mutation(sample_chromosome, dont_flip, allowed_alleles, 1)  # In real life it will be low <- setting 1 to test
    print("Chromosome with 0 or 1 gene mutated")
    print(numpy.matrix(sample_chromosome))

