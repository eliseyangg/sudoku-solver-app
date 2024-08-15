"""
Each sudoku board is represented as a dictionary with string keys and int values.
e.g. my_board['A1'] = 8
"""

ROW = "ABCDEFGHI"
COL = "123456789"
RUNNING_TIMES = []
FAILED = []

def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)

def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def initial_assignment(board):
    # initialize the assignment as board but with its possible domain values -- make consistent
    assignment = {}
    for r in ROW:
        for c in COL:
            if board[r+c] == 0:
                assignment[r+c] = [1,2,3,4,5,6,7,8,9]
            else:
                assignment[r+c] = [board[r+c]]
    # for every variable in assignment
    for domain in assignment:
        # check the ones with initial domains [1,2,3,4,5,6,7,8,9]
        if len(assignment[domain]) > 1:
            # values of interest to have domains checked
            voi = [board[constraining_var] for constraining_var in constraining_vars(domain)]
            for val in voi:
                # remove conflicting items from domains
                if val in assignment[domain] and val != 0:
                    assignment[domain].remove(val)
                    # if a domain is empty, this is not a valid board
                    if len(assignment[domain]) == 1:
                        board[domain] == assignment[domain][0]
                    if len(assignment[domain]) == 0:
                        print("Invalid board!")
                        return None

    return assignment, board

def assignment_to_board(assignment):
    # change the assignment into board style (dict of lists --> dict of ints)
    board = {}
    for var in assignment:
        if len(assignment[var]) == 1:
            board[var] = assignment[var][0]
        else:
            board[var] = 0
    return board

def backtracking(board):
    """Takes a board and returns solved board."""
    a, b = initial_assignment(board)
    return backtrack(a, b)

def backtrack(assignment, board):
    # convert the current assignment to a board to keep for reverting purposes
    curr_board = assignment_to_board(assignment)

    # if all values are filled and non-zero, the goal state has been reached
    if 0 not in curr_board.values():
        return curr_board
    
    # pick minimum remaining value variable to test numbers on
    var = mrv(assignment)

    # least constraining variable: order of numbers to test on
    lcv_list = lcv(var, assignment, board)
    while len(lcv_list)>0:
        
        val = lcv_list.pop(0) # iterate through lcv

        # if board is consistent
        if consistent(val, var, board):
            
            temp_assignment = assignment.copy()
            
            board[var] = val
            curr_board[var]=val

            updated_assignment = forward_check(val, var, temp_assignment, curr_board)
            # if forward checking fails
            if updated_assignment == None: 
                remove_and_restore(val, var, assignment, board)
                # print('fc fail')
                continue # forward check didn't work, move to next value!
            result = backtrack(updated_assignment, board)
            if result != None: 
                return result # keep searching in this branch!
            # if lcv with mrv doesn't work, remove and go back up the branch
            remove_and_restore(val, var, assignment, board) # remove and restores others
    return None 


def mrv(assignment):
    # return the unassigned variable with the minimum remaining values
    domain_lengths = [10 if len(d) == 1 else len(d) for d in assignment.values()]
    return list(assignment.keys())[domain_lengths.index(min(domain_lengths))]

def lcv(var, assignment, board):
    # return the value with the most unknowns (least constraints)
    counts = {v : 0 for v in assignment[var]}
    for val in board:
        if board[val] in counts:
            counts[board[val]] += 1
    lcv_list = dict(sorted(counts.items(), key = lambda x:x[1], reverse = True))
    return list(lcv_list.keys()) 

def constraining_vars(var):
    row = var[0]
    col = var[1]
    # extract in the same row
    same_row = set([row + str(c) for c in range(1,10)])
    # extract in the same column
    same_col = set([ROW[i] + col for i in range(9)])
    # extract in the same box
    top_left_row = ROW.index(row) // 3 * 3
    top_left_col = (int(col)-1) // 3 * 3
    same_box = set([ROW[x] + COL[i] for x in range(top_left_row, top_left_row+3) for i in range(top_left_col, top_left_col+3)])
    return same_row | same_col | same_box - set([var])

def consistent(val, var, board):
    # values of interest that are assigned
    voi = [board[constraining_var] if constraining_var!=var else 10 for constraining_var in constraining_vars(var)]
    if val in voi: # if the lcv is inconsistent with constraint
        return False
    return True # when val is the only value in that row, col, and box

def forward_check(val, var, assignment, board):
    # reduce variable domains to make consistent
    board[var] = val
    assignment[var] = [val]
    for variable in constraining_vars(var):
        if var != variable:
            if val in assignment[variable]:
                assignment[variable].remove(val)
            if len(assignment[variable])==1 and not consistent(assignment[variable][0], variable, board):
                # add back 
                # not consistent with assignment[variable]
                return None
            if len(assignment[variable])==0:
                # variable  has no more items
                return None
    return assignment # when val is the only value in that row, col, and box

def remove_and_restore(val, var, assignment, board): 
    # similar to forward check, but adding values back instead of removing
    board[var] = 0
    assignment[var].remove(val) # remove
    for val_domain_check in constraining_vars(var): # restore if consistent
        # if not constrained, and if adding val would still make it consistent, add it to domain. 
        if board[val_domain_check] == 0 and (val not in assignment[val_domain_check]) and consistent(val, val_domain_check, board):
            assignment[val_domain_check].append(val)
    return

def solve_sudoku(board_string):
    # Parse boards to dict representation, scanning board L to R, Up to Down
    board = {ROW[r] + COL[c]: int(board_string[9*r+c])
                for r in range(9) for c in range(9)}       
    
    solved_board = backtracking(board)
    if solved_board == None:
        return 'invalid board'
    
    return board_to_string(solved_board)