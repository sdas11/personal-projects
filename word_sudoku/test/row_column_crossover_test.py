import numpy
from ga_component.row_column_crossover import crossover

if __name__ == '__main__':
    # Example 1
    parent_a = [
            ['A1', 'A1', 'A12', 'A1'],
            ['A2', 'A2', 'A23', 'A2'],
            ['A3', 'A3', 'A3', 'A3'],
            ['A2', 'A4', 'A4', 'A4']
        ]
    parent_b = [
            ['B1', 'B1', 'B12', 'B13'],
            ['B2', 'B2', 'B2', 'B2'],
            ['B31', 'B32', 'B33', 'B3'],
            ['B4', 'B4', 'B4', 'B4']
        ]

    row_swap_child, col_swap_child = crossover(parent_a, parent_b)
    print(numpy.matrix(row_swap_child))
    print(numpy.matrix(col_swap_child))
    print("Done")
