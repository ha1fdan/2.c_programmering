def printgrid(grid):
    for row in grid:
        print(row)


def floodfill(grid, row, col, value, debug=False):

    if not grid or not grid[0]:
        return

    max_row = len(grid)-1
    max_col = len(grid[0])-1

    if row < 0 or col < 0 or row > max_row or col > max_col:
        return

    org_value = grid[row][col]
    if org_value == value: #would loop infinitely, so we return immediately.
        return
   
    queue = []
    queue.append((row,col))

    while len(queue) > 0:
        node = queue.pop(0)
        row, col = node # unpack tuple

        if debug: 
            print(f"\n# floodfill while-loop with row={row} and col={col}")

        # top 2
        if row < 0 or col < 0:
            if debug:
                print("Skipping because of bounds")
            continue
        # bottom 2
        if row > max_row or col > max_col:
            if debug:
                print("Skipping because of bounds")
            continue
        
        # floodfill to right, left, down, up.
        
        
        if grid[row][col] != org_value:
            if debug:
                print("Skipping because of value")
            continue 

        grid[row][col] = value

        if debug:
            printgrid(grid)

        queue.append((row+1,col)) # ned
        queue.append((row,col+1)) # højre
        queue.append((row-1,col)) # op
        queue.append((row,col-1)) # venstre

if __name__ == "__main__":
    grid = [[0,0,0,0,2,0],
            [0,0,0,0,2,0],
            [0,0,0,0,2,0],
            [0,0,0,0,2,0],
            [2,2,2,2,2,0],
            [0,0,0,0,0,0]
           ]
    floodfill(grid,1,1,3,debug=True)