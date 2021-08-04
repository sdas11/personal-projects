from extra.table_renderer import DEFAULT_FONT_COLOR_MATRIX, DEFAULT_CELL_COLOR_MATRIX, get_table_html, \
    wrap_in_container, render_to_html, wrap_in_horizontal_container, wrap_in_vertical_container
from model.sample_problems import easy_problems


if __name__ == '__main__':
    chromosome = easy_problems[0]

    # Lets create a page with 3 grids in 1 row AND 2 rows in total

    row_string = ""
    for i in range(3):  # 3 grids
        table_html_c = wrap_in_container(get_table_html(
            easy_problems[0], "My Table", DEFAULT_FONT_COLOR_MATRIX, DEFAULT_CELL_COLOR_MATRIX
        ))
        row_string = row_string + table_html_c
    row_string = wrap_in_horizontal_container(row_string)

    column_string = ""
    for i in range(2):  # 2 rows
        column_string = column_string + row_string
    column_string = wrap_in_vertical_container(column_string)

    render_to_html(column_string, "render.html")
