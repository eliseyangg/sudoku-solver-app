import random

def get_empty_board():
    return [{f"col{i+1}": None for i in range(9)} for _ in range(9)]

def get_column_defs():
    return [
        {
            "field": f"col{i+1}",
            "headerName": "",
            "sortable": False,
            "editable": True,
            "columnTypes": "centerAligned",
            "cellStyle": {"text-align": "center", "font-size": "20px", "enableCellChangeFlash":"True"},
        } for i in range(9)
    ]

def get_random_template():
     
    src_filename = 'src/assets/sudokus_start.txt'
    try:
        srcfile = open(src_filename, "r")
        sudoku_file = srcfile.read()
    except:
        print("Error reading the sudoku file %s" % src_filename)
        exit()

    sudoku_list = sudoku_file.split("\n")
    random_string = sudoku_list[random.randint(0, len(sudoku_list)-1)]    
    return random_string

def get_random_row_data():

    random_string = get_random_template()
    empty_row_data = get_empty_board()

    row_data = []
    index = 0
    for row in empty_row_data:
        new_row = {}
        for col_id in row.keys():
            value = int(random_string[index])
            new_row[col_id] = None if value == 0 else value
            index += 1
        row_data.append(new_row)

    return row_data