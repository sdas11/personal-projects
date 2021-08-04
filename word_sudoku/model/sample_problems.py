# Problem difficulty level is anecdotal - from Google Search results
from model.data_types import EmptyGene as Eg

easy_problems = [
    [
        [Eg, 'O', 'W', 'D'],
        [Eg, 'W', Eg, Eg],
        [Eg, Eg, 'R', Eg],
        ['O', 'R', 'D', Eg]
    ],
    [
        ['R', 'D', 'W', Eg],
        [Eg, 'O', Eg, Eg],
        [Eg, Eg, 'O', Eg],
        [Eg, 'W', 'D', 'R']
    ]
]

medium_problems = [
    [
        [Eg, Eg, Eg, 'D'],
        [Eg, Eg, Eg, Eg],
        [Eg, 'R', 'D', Eg],
        [Eg, Eg, Eg, Eg]
    ],
    [
        [Eg, 'W', Eg, 'D'],
        [Eg, Eg, 'W', Eg],
        ['O', Eg, Eg, Eg],
        [Eg, Eg, Eg, Eg]
    ],
    [
        ['W', Eg, 'D', Eg],
        [Eg, Eg, Eg, Eg],
        [Eg, Eg, Eg, Eg],
        [Eg, 'W', Eg, 'O']
    ],
    [
        [Eg, Eg, 'W', Eg],
        ['D', Eg, Eg, Eg],
        [Eg, Eg, Eg, 'O'],
        [Eg, 'R', Eg, Eg]
    ]
]

hard_problems = [
    # https://www.reddit.com/r/sudoku/comments/h9ovdg/worlds_hardest_4x4_micro_sudoku/
    [
        [Eg, Eg, Eg, Eg],
        [Eg, Eg, Eg, Eg],
        ['O', Eg, Eg, 'W'],
        [Eg, Eg, 'D', Eg]
    ],
    # https://nl.pinterest.com/pin/675821487811108301/
    [
        [Eg, Eg, Eg, Eg],
        ['W', Eg, 'O', Eg],
        [Eg, 'D', Eg, 'R'],
        [Eg, Eg, Eg, Eg]
    ]
]

no_solution_problems = [
    # https://www.reddit.com/r/sudoku/comments/kp7r87/this_4x4_that_was_shown_in_a_mobile_ad_for_a/
    [
        ['W', Eg, Eg, Eg],
        [Eg, 'D', Eg, 'O'],
        [Eg, Eg, 'O', Eg],
        ['R', Eg, Eg, 'D']
    ]
]
