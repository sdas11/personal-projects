import math

from util.common import get_sub_matrices
from model.data_types import Chromosome, EmptyGene


def fitness_function(chromosome: Chromosome, min_score: int) -> int:
    """
        This function evaluates the fitness of a chromosome. This function is highly adapted for Sudoku type puzzles.
        Assumptions:
        1. Fitness criteria evaluates for no repetition of elements along rows, columns or "sub-matrices"

        Args:
            chromosome: Input chromosome to evaluate the fitness for - in row matrix form. Example:
            # For a Chromosome [0, 1, 2, 3] row_matrix will be [ [0, 1], [2, 3] ] assuming matrix_size = 2
            min_score: The minimum fitness score to begin with

        Returns:
            description: Fitness score. Maximum possible score is 12.

    """
    mat_size = len(chromosome)
    fitness_score = min_score

    # For the Sudoku type puzzle, we will deduct 1 point for every row which contains 1 or more repeated alleles
    for row in chromosome:
        if len(row) == len(set(row)) and EmptyGene not in row:
            fitness_score = fitness_score + 1

    # For the Sudoku type puzzle, we will deduct 1 point for every column which contains 1 or more repeated alleles
    for col_idx in range(mat_size):
        col = []
        for row_idx in range(mat_size):
            col.append(chromosome[row_idx][col_idx])
        if len(col) == len(set(col)) and EmptyGene not in col:
            fitness_score = fitness_score + 1

    # For the Sudoku type puzzle, we will deduct 1 point for every sub-matrix which contains 1 or more repeated alleles
    sub_matrix_size = int(math.sqrt(mat_size))  # For a 4x4 matrix, sub-matrix will be square_root(4) x square_root(4)
    # get_sub_matrices returns the sub_matrix as a flat list
    sub_matrices = get_sub_matrices(chromosome, sub_matrix_size)
    for sub_matrix in sub_matrices:
        if len(sub_matrix) == len(set(sub_matrix)) and EmptyGene not in sub_matrix:
            fitness_score = fitness_score + 1

    return fitness_score
