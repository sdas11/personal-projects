import random

from model.data_types import allowed_alleles, EmptyGene
from model.sample_problems import easy_problems
from util.common import populate_for_empty_genes

if __name__ == '__main__':
    output_chromosome = populate_for_empty_genes(random.choice(easy_problems), allowed_alleles)
    # Verify, no cell is blank
    found_empty_cell = False
    for idx in range(len(output_chromosome)):
        if output_chromosome[idx] is EmptyGene:
            found_empty_cell = True
            break
    if found_empty_cell:
        print("Test failed")
    else:
        print("Test successful")

