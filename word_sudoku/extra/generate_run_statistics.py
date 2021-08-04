import csv
import math
import numpy

from ga_component.ga_solver import ga_grid_solver
from main_demo import __get_seed_population_and_dont_modify_array, solver_properties
from model.sample_problems import easy_problems, medium_problems, hard_problems, no_solution_problems

if __name__ == '__main__':
    # Select the problem we want to solve
    partial_chromosome_easy = easy_problems[0]
    partial_chromosome_hard = hard_problems[0]

    with open('/Users/gahmed/Desktop/report.csv', mode='a') as csv_file:
        fieldnames = ['max_population', 'selection_strategy', 'num_of_crossovers_per_generation',
                      'mutation_probability', 'problem_difficulty', 'runs', 'average_time(success)', 'success_rate']

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        # writer.writeheader()
        # writer.writerow({'emp_name': 'John Smith', 'dept': 'Accounting', 'birth_month': 'November'})
        # writer.writerow({'emp_name': 'Erica Meyers', 'dept': 'IT', 'birth_month': 'March'})

        runs = 50
        for max_population in range(3, 100):
            for selection_strategy in ['fitness_proportionate_selection', 'simple_sort']:
                if max_population == 3:
                    start_idx = 2
                else:
                    start_idx = 1
                for num_of_crossovers_per_generation in range(start_idx, math.ceil(max_population / 2) + 1):
                    for mutation_probability in [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
                        for problem_difficulty in ['easy', 'hard']:
                            # Start
                            solver_properties['max_population'] = max_population
                            solver_properties['selection_strategy'] = selection_strategy
                            solver_properties['num_of_crossovers_per_generation'] = num_of_crossovers_per_generation
                            solver_properties['mutation_probability'] = mutation_probability

                            if problem_difficulty == 'easy':
                                seed_population, dont_modify = __get_seed_population_and_dont_modify_array(
                                    partial_chromosome_easy, solver_properties)
                            else:
                                seed_population, dont_modify = __get_seed_population_and_dont_modify_array(
                                    partial_chromosome_hard, solver_properties)

                            run_successes = []
                            run_times = []

                            for run in range(runs):
                                solution_found = False
                                try:
                                    solution, solution_found, iterations, time_taken = ga_grid_solver(
                                        seed_population, dont_modify, solver_properties, max_iterations=20000)
                                except Exception:
                                    print("error for solver_props" + str(solver_properties))
                                if solution_found:
                                    run_successes.append(1)
                                    run_times.append(time_taken)
                                else:
                                    run_successes.append(0)

                            average_time = None
                            success_percentage = 0
                            if max(run_successes) == 1:
                                average_time = numpy.mean(run_times)
                                success_percentage = numpy.mean(run_successes) * 100

                            writer.writerow({
                                'max_population': max_population,
                                'selection_strategy': selection_strategy,
                                'num_of_crossovers_per_generation': num_of_crossovers_per_generation,
                                'mutation_probability': mutation_probability,
                                'problem_difficulty': problem_difficulty,
                                'runs': runs,
                                'average_time(success)': average_time,
                                'success_rate': success_percentage
                            })
                            csv_file.flush()

    print("Done")
