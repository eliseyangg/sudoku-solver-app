from helpers.sudoku import solve_sudoku
from helpers.layout import get_empty_board, get_column_defs, get_random_row_data

from dash import Dash, dcc, html, no_update
import dash_ag_grid as dag
from dash.dependencies import Input, Output, State 
import dash_bootstrap_components as dbc 

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])
app.title = 'Elise\'s Sudoku Solver'
server = app.server

app.layout = html.Div([
    dcc.ConfirmDialog(
        id='confirm-invalid',
        message='Invalid board entered.',
    ),
    dbc.Container([
        dbc.Row(
            html.H1('Sudoku Solver'), className="d-flex justify-content-center",
        ),
        dbc.Row(
            dbc.Col(
                dag.AgGrid(
                    id="sudoku-grid",
                    rowData=get_empty_board(),
                    columnDefs=get_column_defs(),
                    defaultColDef={"resizable": False, "editable": True, "enableCellChangeFlash": True},
                    style={"height": "450px", "width": "450px", "margin": "auto"},
                    className="ag-theme-balham sudoku-grid",
                    dashGridOptions={
                        "columnHoverHighlight": True,
                        "suppressRowClickSelection": True,
                        "suppressColumnVirtualisation": True,
                        "suppressHorizontalScroll": True,
                        "domLayout": "autoHeight",
                        "suppressMenuHide": True,
                        "headerHeight": 0,
                        "rowHeight": 50,
                    },
                    columnSize="sizeToFit",
                ),
                width="auto",
                className="d-flex justify-content-center"
            ),
            className="mb-3"
        ),
        dbc.Row(
            dbc.Col(
                [dbc.Button("Clear", color="secondary", style={"border-radius": "99px", "margin":'5px'}, id="button-reset"),
                 dbc.Button("Random Template", color="secondary", style={"border-radius": "99px", "margin":'5px'}, id="button-random"),
                 dbc.Button("Solve", color="primary", style={"border-radius": "99px", "margin":'5px'}, id="button-solve"),],
                width="auto",
                className="d-flex justify-content-center",
            ),
        ),
    ], 
    className="d-flex flex-column justify-content-center align-items-center vh-100")
])


# CALLBACK: Cell input validation
@app.callback(
    Output("sudoku-grid", "rowData", allow_duplicate=True),
    Input("sudoku-grid", "cellValueChanged"),
    State("sudoku-grid", "rowData"),
    prevent_initial_call=True,
)
def validate_input(cell_value_changed_list, row_data):
    if not cell_value_changed_list:
        return no_update

    cell_change = cell_value_changed_list[0]
    try:
        value = int(cell_change['value'])
    except:
        value = None
    row_index = cell_change['rowIndex']
    col_id = cell_change['colId']

    row_data[row_index][col_id] = None if value is not None and (value < 1 or value > 9) else value

    return row_data

# CALLBACK: Reset or fill random cells
@app.callback(
    Output("sudoku-grid", "rowData", allow_duplicate=True),
    Input("button-reset", "n_clicks"),
    prevent_initial_call=True,
)
def reset_board(_):
    return get_empty_board()
    
# CALLBACK: Reset or fill random cells
@app.callback(
    Output("sudoku-grid", "rowData", allow_duplicate=True),
    Input("button-random", "n_clicks"),
    prevent_initial_call=True,
)
def reset_board(_):
    return get_random_row_data()


# CALLBACK: Solve
@app.callback(
    Output('sudoku-grid', 'rowData'),
    Output('confirm-invalid', 'displayed'),
    Input('button-solve', 'n_clicks'), 
    State('sudoku-grid', 'rowData')
)
def solve_and_update_sudoku(n_clicks, row_data):
    if not n_clicks:
        return no_update, False

    sudoku_string = ''.join(
        str(cell if cell is not None else 0)
        for row in row_data
        for cell in row.values()
    )

    solved_string = solve_sudoku(sudoku_string)
    if solved_string == 'invalid board':
        return no_update, True

    new_row_data = []
    index = 0
    for row in row_data:
        new_row = {}
        for col_id in row.keys():
            solved_value = int(solved_string[index])
            new_row[col_id] = solved_value
            index += 1
        new_row_data.append(new_row)

    return new_row_data, False



if __name__ == '__main__':
    app.run(debug=True)