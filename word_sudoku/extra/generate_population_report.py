import copy
import numpy

from extra.html_snippets import ColorPaletteRed, ColorPaletteGreen, DarkRed, ColorPaletteBlack
from extra.table_renderer import wrap_in_container, wrap_in_vertical_container, wrap_in_horizontal_container, \
    get_table_html, DEFAULT_FONT_COLOR_MATRIX, DEFAULT_CELL_COLOR_MATRIX, render_to_html
from ga_component.ga_solver_with_debug import ga_grid_solver_debug
from main_demo import __get_problem_to_solve, solver_properties, __get_seed_population_and_dont_modify_array
from model.sample_problems import hard_problems, medium_problems


def __check_key_exists(dict_obj, key):
    try:
        dict_obj[key]
        return True
    except KeyError:
        return False


def __darken_dont_modify(_dont_modify, font_color_matrix=copy.deepcopy(DEFAULT_CELL_COLOR_MATRIX)) -> \
        list[list[str]]:
    for row_idx in range(len(font_color_matrix)):
        for col_idx in range(len(font_color_matrix[row_idx])):
            if _dont_modify[row_idx][col_idx]:
                font_color_matrix[row_idx][col_idx] = ColorPaletteBlack[1]

    return font_color_matrix


def __get_color_matrix_for_row_child(parent1, color_par_1, color_par_2, child, _dont_modify) -> list[list[str]]:
    color_matrix = []
    _mat_size = len(parent1)
    for row_idx in range(_mat_size):
        if numpy.array_equal(parent1[row_idx], child[row_idx]):
            color_matrix.append([color_par_1] * _mat_size)
        else:
            color_matrix.append([color_par_2] * _mat_size)

    return __darken_dont_modify(_dont_modify, color_matrix)


def __get_color_matrix_for_col_child(parent1, colorParent1, colorParent2, child, _dont_modify) -> list[list[str]]:
    color_matrix = []
    parent1_t = numpy.array(parent1).transpose()
    child_t = numpy.array(child).transpose()
    _mat_size = len(parent1_t)
    for t_row_idx in range(_mat_size):
        if numpy.array_equal(parent1_t[t_row_idx], child_t[t_row_idx]):
            color_matrix.append([colorParent1] * _mat_size)
        else:
            color_matrix.append([colorParent2] * _mat_size)

    return __darken_dont_modify(_dont_modify, numpy.array(color_matrix).transpose())


def __add_selection_row(debug_entry, row_elements, _dont_modify):
    if debug_entry['selection_happened']:
        row_elements.append(wrap_in_horizontal_container(
            wrap_in_container("<span>Population after selection</span>"))
        )
        pop_after_selection_html = ""
        idx = 0
        for chromosome in debug_entry['population_after_selection']:
            pop_after_selection_html = pop_after_selection_html + wrap_in_container(get_table_html(
                chromosome, "Id: " + str(idx), DEFAULT_FONT_COLOR_MATRIX, __darken_dont_modify(_dont_modify)
            ))
            idx = idx + 1
        row_elements.append(wrap_in_horizontal_container(pop_after_selection_html))
    else:
        row_elements.append(wrap_in_horizontal_container(
            wrap_in_container(
                "<span>Selection Skipped (no mutation or crossover happened in previous generation)</span>"))
        )


def __add_crossover_row(crossover_data, population, row_elements, _dont_modify):
    row_elements.append(wrap_in_horizontal_container(wrap_in_container("<span>Crossovers</span>")))
    for crossover_entry in crossover_data:
        if crossover_entry['crossover_done']:
            # crossover_row_string
            parent_id_1 = crossover_entry['parent_id_1']
            parent_id_2 = crossover_entry['parent_id_2']

            _mat_size = len(population[parent_id_1])

            crs = wrap_in_container(get_table_html(
                population[parent_id_1], "Parent - Id: " + str(parent_id_1), DEFAULT_FONT_COLOR_MATRIX,
                __darken_dont_modify(
                    _dont_modify, [[ColorPaletteRed[0] for i_t in range(_mat_size)] for j_t in range(_mat_size)]
                )

            ))

            crs = crs + wrap_in_container("+")

            crs = crs + wrap_in_container(get_table_html(
                population[parent_id_2], "Parent - Id: " + str(parent_id_2), DEFAULT_FONT_COLOR_MATRIX,
                __darken_dont_modify(
                    _dont_modify, [[ColorPaletteGreen[0] for i_t in range(_mat_size)] for j_t in range(_mat_size)]
                )
            ))

            crs = crs + wrap_in_container("=")

            crs = crs + wrap_in_container(get_table_html(
                crossover_entry['row_swap_child'], "Row Swap Child - Id: " + str(crossover_entry['row_swap_child_id']),
                DEFAULT_FONT_COLOR_MATRIX,
                __get_color_matrix_for_row_child(
                    population[parent_id_1], ColorPaletteRed[0], ColorPaletteGreen[0],
                    crossover_entry['row_swap_child'], _dont_modify
                )
            ))

            crs = crs + wrap_in_container("&")

            crs = crs + wrap_in_container(get_table_html(
                crossover_entry['col_swap_child'],
                "Column Swap Child - Id: " + str(crossover_entry['col_swap_child_id']),
                DEFAULT_FONT_COLOR_MATRIX,
                __get_color_matrix_for_col_child(
                    population[parent_id_1], ColorPaletteRed[0], ColorPaletteGreen[0],
                    crossover_entry['col_swap_child'], _dont_modify
                )
            ))

            row_elements.append(wrap_in_horizontal_container(crs))
        else:
            row_elements.append(wrap_in_horizontal_container(
                wrap_in_container("<span>1 crossover skipped due to identical parents (after random selection) "
                                  "for mating</span>")))


def __add_mutation_row(mutation_data, population_before, population_after, row_elements, _dont_modify):
    if len(mutation_data) > 0:
        row_elements.append(wrap_in_horizontal_container(wrap_in_container("<span>Mutations</span>")))
    else:
        row_elements.append(wrap_in_horizontal_container(wrap_in_container("<span>No mutations happened</span>")))
    for mutation_entry in mutation_data:
        chromosome_idx = mutation_entry['population_idx']
        row_idx = mutation_entry['flip_row_idx']
        col_idx = mutation_entry['flip_col_idx']

        font_color_matrix = copy.deepcopy(DEFAULT_FONT_COLOR_MATRIX)
        font_color_matrix[row_idx][col_idx] = DarkRed
        # mutation row string
        mrs = wrap_in_container(get_table_html(
            population_before[chromosome_idx], "Id: " + str(chromosome_idx), font_color_matrix,
            __darken_dont_modify(_dont_modify)
        ))

        mrs = mrs + wrap_in_container("->")

        mrs = mrs + wrap_in_container(get_table_html(
            population_after[chromosome_idx], "Id: " + str(chromosome_idx), font_color_matrix,
            __darken_dont_modify(_dont_modify)
        ))

        row_elements.append(wrap_in_horizontal_container(mrs))
    pass


def __append_intro_to_html_body(_html_body, _problem, _dont_modify, _properties, _iterations, _time_taken):
    # Introduction Row Elements
    intro_row_elements = [
        wrap_in_horizontal_container(
            wrap_in_container(get_table_html(_problem,
                                             "Partial Word Sudoku", DEFAULT_FONT_COLOR_MATRIX,
                                             __darken_dont_modify(_dont_modify)))
        ),
        wrap_in_horizontal_container(
            "<span>Maximum population per GA iteration: " + str(_properties['max_population']) + "</span><br>" +
            "<span>Selection Strategy: " + str(_properties['selection_strategy']) + "</span><br>" +
            "<span>Number of Crossovers per generation: " +
            str(_properties['num_of_crossovers_per_generation']) + "</span><br>" +
            "<span>Mutation Probability for EACH individual in EACH Iteration: " +
            str(_properties['mutation_probability']) + "</span><br>"
        ),
        wrap_in_horizontal_container(
            "<span>Time taken: " + str(_time_taken) + " secs</span><br>" +
            "<span>Iterations taken to find solution: " + str(iterations) + "</span><br>"
        ),
        wrap_in_horizontal_container(
            "<span style='color:blue'>Please note that the numeric 'id' mentioned for Word Sudoku's are only "
            "valid for 1 generation/iteration - there is no link between ids of 2 separate generations</span>"
        ),
        wrap_in_horizontal_container(
            "<span>Due to file size limits, this run summary was done for max_population = 5 - the actual code "
            "has max_population = 8 per generation</span>"
        )
    ]
    intro_row = ""
    for intro_row_element in intro_row_elements:
        intro_row = intro_row + intro_row_element

    return _html_body + wrap_in_vertical_container(intro_row)


def __append_solution_to_html_body(_html_body, _solution, _dont_modify):
    solution_row_elements = [
        wrap_in_horizontal_container(wrap_in_container("<br><br><hr><h3>End of Iterations</h3><br>")),
        wrap_in_horizontal_container(
            wrap_in_container(get_table_html(_solution,
                                             "Final Solution", DEFAULT_FONT_COLOR_MATRIX,
                                             __darken_dont_modify(_dont_modify)))
        ),
    ]
    solution_row = ""
    for solution_row_element in solution_row_elements:
        solution_row = solution_row + solution_row_element

    return _html_body + wrap_in_vertical_container(solution_row)


def __append_seed_population_row_to_html_body(_html_body, _population, _dont_modify):
    pop_after_seeding_html = ""
    idx = 0
    for chromosome in _population:
        pop_after_seeding_html = pop_after_seeding_html + wrap_in_container(get_table_html(
            chromosome, "Id: " + str(idx), DEFAULT_FONT_COLOR_MATRIX, __darken_dont_modify(_dont_modify)
        ))
        idx = idx + 1

    seed_population_row = wrap_in_horizontal_container(wrap_in_container(
        "<br><br><br><hr><h3>Initial Population (2 x max population)</h3><br><span>Filling random values for "
        "the empty genes in the original puzzle</span>")) + \
        wrap_in_horizontal_container(pop_after_seeding_html)
    return _html_body + wrap_in_vertical_container(seed_population_row)


if __name__ == '__main__':
    # For the report, we want a solution with shorter iterations (due to size limits) - hence keep trying till
    # a short solution is found
    for i in range(1000):
        # Lets render everything into a report
        html_body = ""
        debug_data = {}

        partial_chromosome = medium_problems[1]
        seed_population, dont_modify = __get_seed_population_and_dont_modify_array(partial_chromosome,
                                                                                   solver_properties)

        # Run ga_grid_solver
        solution, solution_found, iterations, time_taken = ga_grid_solver_debug(seed_population, dont_modify,
                                                                                solver_properties,
                                                                                # For the report, we want a solution
                                                                                # with shorter iterations
                                                                                max_iterations=31,
                                                                                debug_data=debug_data)

        if not solution_found:
            continue
        if iterations > 100:
            continue

        debug_list = debug_data['debug_iterations']
        selection_skipped_check = False
        for run_idx in range(len(debug_list)):
            debug_entry = debug_list[run_idx]
            if not debug_entry['selection_happened']:
                selection_skipped_check = True
        if not selection_skipped_check:
            continue

        html_body = __append_intro_to_html_body(html_body, partial_chromosome, dont_modify, solver_properties,
                                                iterations, time_taken)

        html_body = __append_seed_population_row_to_html_body(html_body, debug_data['seed_population'], dont_modify)


        for run_idx in range(len(debug_list)):
            html_row_elements = [
                wrap_in_horizontal_container(wrap_in_container(
                    "<br><br><br><hr><h3>Generation " + str(run_idx) + "</h3>"))
            ]

            debug_entry = debug_list[run_idx]

            # Selection
            __add_selection_row(debug_entry, html_row_elements, dont_modify)

            # Crossover
            if __check_key_exists(debug_entry, 'crossover'):
                __add_crossover_row(debug_entry['crossover'], debug_entry['population_after_crossover'],
                                    html_row_elements, dont_modify)

            # Mutation
            if __check_key_exists(debug_entry, 'mutation'):
                __add_mutation_row(debug_entry['mutation'], debug_entry['population_after_crossover'],
                                   debug_entry['population_after_mutation'], html_row_elements, dont_modify)

            vertical_str = ""
            for html_row_element in html_row_elements:
                vertical_str = vertical_str + html_row_element

            html_body = html_body + wrap_in_vertical_container(vertical_str)

            for_loop_end = 0

        html_body = __append_solution_to_html_body(html_body, solution, dont_modify)

        render_to_html(html_body, "render.html")
        exit(0)
