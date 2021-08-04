import copy
import random
from model.data_types import Chromosome, BooleanMatrix, EmptyGene, allowed_alleles
from model.sample_problems import hard_problems, easy_problems, medium_problems


def ask_user_or_select_random_problem():
    partial_grid = []
    val = input("Do you want to enter your own 4x4 Word Sudoku? Enter 'y' or 'n'. "
                "If you press 'n' a random problem will be chosen\n")
    if val == 'y':
        for row_idx in range(4):
            print("Enter column values for row: " + row_idx)
            col = []
            for col_idx in range(4):
                val = input("Enter one of 'w', 'o', 'r', 'd' or 'x' for blank")
                if val == 'x':
                    col.append(EmptyGene)
                else:
                    col.append(str(val).upper())
            partial_grid.append(col)
    else:
        val = input("Random sudoku will be chosen. Type 'm' for medium, 'h' for hard sudoku. Press any key for easy.\n")
        if val == 'm':
            partial_grid = random.choice(medium_problems)
        elif val == 'h':
            partial_grid = random.choice(hard_problems)
        else:
            partial_grid = random.choice(easy_problems)

    return partial_grid


# Reference for utility code for getting sub-matrix:
# https://onestepcode.com/sudoku-solver-python/ (Code adapted directly from this reference)
def get_sub_matrices(square_matrix: list, sub_mat_size: int) -> list:
    """
    Assume below 2-D square array (matrix)
    [
        ['D' 'O' 'R' 'W'],
        ['W' 'R' 'O' 'D'],
        ['O' 'D' 'W' 'R'],
        ['R' 'W' 'D' 'O']
    ]

    get_sub_matrices(square_matrix, 2) will return an array of 4 lists - each containing the elements of respective 2x2
    sub_matrix
    [
        ['D', 'O', 'W', 'R'],
        ['R', 'W', 'O', 'D'],
        ['O', 'D', 'R', 'W'],
        ['W', 'R', 'D', 'O']
    ]

    :param square_matrix: 2-D array as an array of 4 lists - each denoting a respective row
    :param sub_mat_size: The size into which the sub-grid has to be divided into
    :return:
        sub_matrices: 2-D array with each row as a vector/array/list of elements of respective sub-grids
    """
    sub_matrices = []
    for box_i in range(sub_mat_size):
        for box_j in range(sub_mat_size):
            sub_matrix = []
            for i in range(sub_mat_size):
                for j in range(sub_mat_size):
                    sub_matrix.append(square_matrix[sub_mat_size * box_i + i][sub_mat_size * box_j + j])
            sub_matrices.append(sub_matrix)

    return sub_matrices


def get_bool_matrix_for_filled_cells(square_matrix: list[list]) -> BooleanMatrix:
    bool_matrix = []
    for row in square_matrix:
        bool_row = []
        for cell in row:
            bool_row.append(True) if cell is not EmptyGene else bool_row.append(False)
        bool_matrix.append(bool_row)

    return bool_matrix


def populate_for_empty_genes(chromosome: Chromosome, alleles: allowed_alleles) -> Chromosome:
    output_chromosome = copy.deepcopy(chromosome)
    for row in output_chromosome:
        for row_idx in range(len(output_chromosome)):
            if row[row_idx] is EmptyGene:
                row[row_idx] = random.choice(alleles)

    return output_chromosome
