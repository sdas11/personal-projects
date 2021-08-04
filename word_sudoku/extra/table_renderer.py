from extra.html_snippets import DarkBlack, HtmlSudokuTable, HtmlPage, White
from model.data_types import Chromosome

DEFAULT_FONT_COLOR_MATRIX = [[DarkBlack for i in range(4)] for j in range(4)]
DEFAULT_CELL_COLOR_MATRIX = [[White for i in range(4)] for j in range(4)]


def wrap_in_container(some_html: str):
    return "<div>" + some_html + "</div>"


def wrap_in_vertical_container(some_html: str):
    return '<div class="arrange-horizontal">' + some_html + "</div>"  # yes, horizontal flex means vertical arrangement


def wrap_in_horizontal_container(some_html: str):
    return '<div class="arrange-vertical">' + some_html + "</div>"


def get_table_html(chromosome: Chromosome, table_name: str, font_color_matrix: list[list[str]],
                   cell_color_matrix: list[list[str]]):
    table_string = HtmlSudokuTable
    mat_size = len(chromosome)
    for row_idx in range(mat_size):
        for col_idx in range(mat_size):
            table_string = table_string.replace("{bg-color-" + str(row_idx) + "-" + str(col_idx) + "}",
                                                cell_color_matrix[row_idx][col_idx])
            table_string = table_string.replace("{color-" + str(row_idx) + "-" + str(col_idx) + "}",
                                                font_color_matrix[row_idx][col_idx])
            table_string = table_string.replace("{cell-" + str(row_idx) + "-" + str(col_idx) + "}",
                                                chromosome[row_idx][col_idx])
    table_string = table_string.replace("{caption}", table_name)
    return table_string


def render_to_html(some_html_body: str, file_path: str):
    html_file = open(file_path, "w")
    html_page = HtmlPage
    html_page = html_page.replace("{body-placeholder}", some_html_body)
    html_file.write(html_page)
    html_file.close()
