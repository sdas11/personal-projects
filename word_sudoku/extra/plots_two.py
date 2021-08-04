import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def __make_xlabel_visible_subplot(facet_grid):
    _g = facet_grid
    xlabels, ylabels = [], []
    for ax in _g.axes[-1, :]:
        xlabel = ax.xaxis.get_label_text()
        xlabels.append(xlabel)
    for ax in _g.axes[:, 0]:
        ylabel = ax.yaxis.get_label_text()
        ylabels.append(ylabel)

    for i in range(len(xlabels)):
        for j in range(len(ylabels)):
            _g.axes[j, i].xaxis.set_label_text(xlabels[i])
            # _g.axes[j, i].yaxis.set_label_text(ylabels[j])


def __make_tick_visible_subplot(facet_grid):
    _g = facet_grid
    for ax in _g.axes.flat:
        ax.tick_params(labelleft=True)
        ax.tick_params(labelbottom=True)


def __render_scatter_plot(df_ga):
    df_ga = df_ga.rename(columns={'num_of_crossovers_per_generation': 'crsvr', 'selection_strategy': 'sel_strat'})
    df_ga['sel_strat'] = df_ga['sel_strat'].str.replace('fitness_proportionate_selection', 'fps')
    df_ga['sel_strat'] = df_ga['sel_strat'].str.replace('simple_sort', 'sort')
    facet_grid = sns.FacetGrid(df_ga) \
        .map(plt.scatter, "mutation_probability", "average_time(success)", alpha=0.5).add_legend()
    facet_grid = sns.FacetGrid(df_ga) \
        .map(plt.scatter, "mutation_probability", "success_rate", alpha=0.5).add_legend()
    return facet_grid


if __name__ == '__main__':
    headers = ['max_population', 'selection_strategy', 'num_of_crossovers_per_generation',
               'mutation_probability', 'problem_difficulty', 'runs', 'average_time(success)', 'success_rate']
    dtypes = {
        "selection_strategy": "category",
        "problem_difficulty": "category"
    }
    df = pd.read_csv(
        './run-statistics.csv',
        dtype=dtypes,
        usecols=list(dtypes) + ['max_population', 'num_of_crossovers_per_generation',
                                'mutation_probability', 'runs', 'average_time(success)', 'success_rate']
    )

    # grouping = df.groupby(['selection_strategy', 'num_of_crossovers_per_generation', 'mutation_probability',
    #                        'problem_difficulty', 'runs']).size()

    df_easy = df[df['problem_difficulty'] == 'easy']
    # df_easy = df_easy[df_easy['mutation_probability'] == 0.2]
    df_easy = df_easy[df_easy['max_population'] == 5]
    df_easy = df_easy[df_easy['num_of_crossovers_per_generation'] == 2]
    df_easy = df_easy[df_easy['selection_strategy'] == 'fitness_proportionate_selection']
    df_hard = df[df['problem_difficulty'] == 'hard']
    # df_hard = df_hard[df_hard['mutation_probability'] == 0.2]
    df_hard = df_hard[df_hard['max_population'] == 5]
    df_hard = df_hard[df_hard['num_of_crossovers_per_generation'] == 2]
    df_hard = df_hard[df_hard['selection_strategy'] == 'fitness_proportionate_selection']

    # To just show crsvr and sel_strat values without labels
    # [plt.setp(ax.texts, text="") for ax in facet_grid_hard.axes.flat]
    # facet_grid_hard.set_titles(row_template='{row_name}', col_template='{col_name}')

    # easy_plot = __render_scatter_plot(df_easy)
    # __make_tick_visible_subplot(easy_plot)
    # __make_xlabel_visible_subplot(easy_plot)
    # plt.subplots_adjust(hspace=0.4)
    # plt.subplots_adjust(wspace=0.2)
    # plt.show()

    hard_plot = __render_scatter_plot(df_hard)
    __make_tick_visible_subplot(hard_plot)
    __make_xlabel_visible_subplot(hard_plot)
    plt.subplots_adjust(hspace=0.5)
    plt.show()
