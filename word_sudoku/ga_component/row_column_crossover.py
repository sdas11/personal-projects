import numpy
import random

from model.data_types import Chromosome


def __score(one_dim_list: list):
    return len(set(one_dim_list))  # score = number of distinct elements in list
    # (its fine to count EmptyGene as distinct element - since it denotes the space for a potential solution gene)


def __row_swap(parent_1: Chromosome, parent_2: Chromosome) -> Chromosome:
    """
    Child (Offspring) swaps its empty rows with the best row out of row(parent1) or row(parent2)
    """
    mat_size = len(parent_1)
    row_swapped_child = []
    # Prepare row swapped child
    for row_idx in range(mat_size):
        row_score_parent1 = __score(parent_1[row_idx])
        row_score_parent2 = __score(parent_2[row_idx])

        selected_parent = None
        if row_score_parent1 == row_score_parent2:
            # if scores are equal, 50-50 chance of either row selection
            selected_parent = parent_1 if random.random() <= 0.5 else parent_2
        else:
            selected_parent = parent_1 if row_score_parent1 > row_score_parent2 else parent_2

        # Perform the copy
        row_copy = []
        for row_element in selected_parent[row_idx]:
            row_copy.append(row_element)
        row_swapped_child.append(row_copy)

    return row_swapped_child


def crossover(parent1: Chromosome, parent2: Chromosome) -> tuple[Chromosome, Chromosome]:
    """
    Crossover operator - ALWAYS creates 2 children (row swapped and column swapped)
    :return
        row_swapped_child: Child (Offspring) 1
        col_swapped_child: Child (Offspring) 2
    """
    # Prepare row swapped child
    row_swapped_child = __row_swap(parent1, parent2)

    # Prepare column swapped child
    # First transpose rows -> columns and columns -> rows
    parent1_t = numpy.array(parent1).transpose()
    parent2_t = numpy.array(parent2).transpose()
    col_swapped_child = __row_swap(parent1_t, parent2_t)

    # Transpose back to original and cast numpy.array raw type back to Chromosome type
    col_swapped_child = Chromosome(numpy.array(col_swapped_child).transpose())

    return row_swapped_child, col_swapped_child
