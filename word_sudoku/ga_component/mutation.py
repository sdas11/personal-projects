import random
import copy
from model.data_types import BooleanMatrix, Chromosome, allowed_alleles


def flip_mutation(chromosome: Chromosome, dont_flip: BooleanMatrix, alleles: allowed_alleles, flip_probability: float) \
        -> tuple[bool, int, int]:
    """
    Randomly selects a gene in the chromosome, and mutates it to a different allele.
    :param chromosome: The chromosome on which to perform the mutation.
    :param dont_flip: This prevents certain genes from being mutated.
    :param alleles: List of all alleles which a gene can can hold.
    :param flip_probability: The chance of mutation occuring.
    :return:
        mutation_happened: A boolean answering whether a mutation happened or not
        rand_row_idx1, rand_col_idx1: Row and Column Indices of the gene (cell) where mutation happened
    """
    mutation_happened = False
    mat_size = len(chromosome)

    # To return the indices where mutation happened (if it happens)
    rand_row_idx1, rand_col_idx1 = (None, None)

    if random.random() < flip_probability:
        allowed_to_flip_genes = []

        # Populate allowed_to_flip_genes
        for row_idx in range(mat_size):
            for col_idx in range(len(chromosome[row_idx])):
                if not dont_flip[row_idx][col_idx]:
                    allowed_to_flip_genes.append((row_idx, col_idx))

        # Select any random gene from allowed_to_flip_genes
        rand_row_idx1, rand_col_idx1 = random.choice(allowed_to_flip_genes)

        # Select random new allele
        available_choices = copy.deepcopy(alleles)
        # Remove existing allele from a copy of allowed_alleles (choices) first
        available_choices.remove(chromosome[rand_row_idx1][rand_col_idx1])
        chromosome[rand_row_idx1][rand_col_idx1] = random.choice(available_choices)

        mutation_happened = True

    return mutation_happened, rand_row_idx1, rand_col_idx1
