rows = 'ABCDEFGHI'
cols = '123456789'
'''
Added an extra variable to explicitly
declare the inverted array of columns
'''
cols_inverted = cols[::-1]

# Need to define the function before making assignments
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
'''
Created the main diagonal units in order to solve the 
diagonal sudoku problem
'''
main_diagonal_units = [rows[i] + cols[i] for i in range(0, len(rows))]
'''
Created the reverse diagonal units in order to solve the 
diagonal sudoku problem
'''
reverse_diagonal_units = [rows[i] + cols_inverted[i] for i in range(0, len(rows))]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
'''
Added the main diagonal units and the reverse diagonal units
to the unitlist. Used the implicit parsing to make it a list and avoid the
type error
'''
unitlist = row_units + column_units + square_units + [main_diagonal_units] + [reverse_diagonal_units]
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    for key, value in values.items():
        # search for the boxes which value is length 2
        if len(value) == 2:
            # once the box is found loop over its units to find
            # another box that contains the same value
            for unit in units[key]:
                # initialize the counter 1, which already counts the
                # original value
                cnt = 1
                # loop over each of the boxes in a given unit
                for box in unit:
                    # check if the value in the current box
                    # is the same as the original value AND the current box is not
                    # the same as the key
                    if values[box] == value and key != box:
                        # increment the amount of similar values by 1
                        cnt += 1
                # if there is exactly one box which contains the same value
                # as the original one (with 2 characters)
                if cnt == 2:
                    # val0 will contain the first character
                    val0 = value[0]
                    # val1 will contain the second character
                    val1 = value[1]
                    # THIS IS A BIT INEFFICIENT
                    # loop again through the boxes in the unit and replace
                    # the characters as required by the heuristic
                    for box in unit:
                     # Eliminate the naked twins as possibilities for their peers
                        if values[box] != value:
                            values[box] = values[box].replace(val0, '')
                            values[box] = values[box].replace(val1, '')
    return values
    
def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    # Create a dictionary with the values fill with the number assigned to the box
    # or with '123456789' if the box is originally empty
    return {boxes[idx]: val if val != '.' else '123456789' for idx, val in enumerate(grid)}

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    # loop through all the boxes (it is a dictionary)
    for key, value in values.items():
        # if the box is already solved
	    if(len(value) == 1):
		    for peer in peers[key]:
                # make sure you remove value from all the other boxes
                # in the set of peers
		        values[peer] = values[peer].replace(value, '')
    return values

def only_choice(values):
    # loop through every unit in our list
    for unit in unitlist:
        # check in how many boxes a specific digit appears
        for digit in '123456789':
            digit_places = [box for box in unit if digit in values[box]]
            if(len(digit_places) == 1):
                values[digit_places[0]] = digit
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    # Using depth-first search and propagation, create a search tree and solve the sudoku.
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid) # Transform the grid into a board
    reduced_values = reduce_puzzle(values) # Reduce the values with the basic constraints (elimination)
    return search(reduced_values) # Apply further logic using search to solve the problem.

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
