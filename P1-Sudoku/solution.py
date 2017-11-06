from itertools import chain

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if 1 or len(value) == 1:
        assignments.append(values.copy())
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A
                for b in B]

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units    = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') 
                              for cs in ('123','456','789')]
diag_units = [[r+c for r, c in zip(rows, cols)],
              [r+c for r, c in zip(rows, reversed(cols))]]
unitlist = row_units + column_units + square_units + diag_units

units = {box: [unit for unit in unitlist 
                    if box in unit]
         for box in boxes}

peers = {box: set(chain(*units[box])) - set([box])
         for box in boxes}

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
    values = ['123456789' if box == '.' else box
              for box in grid]

    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[box]) for box in boxes)   
    line = '+'.join(['-' * (width*3)] * 3)
    for r in rows:
        print(''.join(values[r+c].center(width) + ('|' if c in '36' else '')
              for c in cols))
        if r in 'CF': print(line)

def eliminate(values):
    solved = [box for box in values 
                  if len(values[box]) == 1]
    for box in solved:
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(values[box],''))
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            appearances = [box for box in unit 
                               if digit in values[box]]
            if len(appearances) == 1:
                assign_value(values, appearances[0], digit)
    return values

def naked_twins(values):
    for unit in unitlist:
        twos = {box: values[box] for box in unit
                                 if len(values[box]) == 2}
        if len(twos) == 2 and len(set(twos.values())) == 1:
            twins = list(twos.values())[0]
            for box in unit:
                if box not in twos:
                    new_value = values[box]
                    for twin in twins:
                        new_value = new_value.replace(twin, '')
                    assign_value(values, box, new_value)
    return values 

def count_box(values, n):
    return sum(len(v) == n for v in values.values())

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        before = count_box(values, 1)
        values = naked_twins(only_choice(eliminate(values)))
        after  = count_box(values, 1)
        stalled = before == after

        if count_box(values, 0): return False
    return values

def search(values):
    values = reduce_puzzle(values)
    
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    
    n, s = min((len(values[s]), s) for s in boxes 
                                   if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    return search(grid_values(grid))

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
