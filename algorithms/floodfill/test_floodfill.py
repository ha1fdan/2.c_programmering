from floodfill import floodfill

# Fylder én celle omgivet af vægge
def test_ff_full_boundaries():
    grid = [[1,1,1],
            [1,0,1],
            [1,1,1]]

    expected = [[1,1,1],
                [1,2,1],
                [1,1,1]]

    floodfill(grid,1,1,2)

    assert grid == expected

# Fylder fire celler omgivet af vægge
def test_ff_full_boundaries2():
    grid = [[1,1,1,1],
            [1,0,0,1],
            [1,0,0,1],
            [1,1,1,1]]

    expected = [[1,1,1,1],
                [1,2,2,1],
                [1,2,2,1],
                [1,1,1,1]]

    floodfill(grid,1,1,2)

    assert grid == expected

# Fylder hele gitteret når alle celler har samme værdi
def test_ff_fill_entire_grid():
    grid = [[0,0,0],
            [0,0,0],
            [0,0,0]]

    expected = [[1,1,1],
                [1,1,1],
                [1,1,1]]

    floodfill(grid, 0, 0, 1)

    assert grid == expected

# Gitteret forbliver uændret når ny værdi er lig den gamle
def test_ff_same_value_no_change():
    grid = [[1,1,1],
            [1,1,1],
            [1,1,1]]

    expected = [[1,1,1],
                [1,1,1],
                [1,1,1]]

    floodfill(grid, 1, 1, 1)

    assert grid == expected

# Starter fra et hjørne og stopper ved en væg
def test_ff_corner_start():
    grid = [[0,0,1],
            [0,0,1],
            [1,1,1]]

    expected = [[2,2,1],
                [2,2,1],
                [1,1,1]]

    floodfill(grid, 0, 0, 2)

    assert grid == expected

# Fyldningen krydser ikke en lodret væg
def test_ff_does_not_cross_boundary():
    grid = [[0,0,2,0,0],
            [0,0,2,0,0],
            [0,0,2,0,0]]

    expected = [[1,1,2,0,0],
                [1,1,2,0,0],
                [1,1,2,0,0]]

    floodfill(grid, 0, 0, 1)

    assert grid == expected

# Fylder et gitter med kun én celle
def test_ff_single_cell_grid():
    grid = [[0]]

    expected = [[5]]

    floodfill(grid, 0, 0, 5)

    assert grid == expected

# Fylder en enkelt vandret række
def test_ff_single_row():
    grid = [[0,0,0,0,0]]

    expected = [[3,3,3,3,3]]

    floodfill(grid, 0, 2, 3)

    assert grid == expected

# Fylder en enkelt lodret kolonne
def test_ff_single_column():
    grid = [[0],[0],[0],[0]]

    expected = [[7],[7],[7],[7]]

    floodfill(grid, 1, 0, 7)

    assert grid == expected

# Isoleret område bag vægge forbliver uændret
def test_ff_island_untouched():
    grid = [[0,0,0,1,0],
            [0,0,0,1,0],
            [1,1,1,1,1],
            [0,1,0,0,0],
            [0,1,0,0,0]]

    floodfill(grid, 0, 0, 2)

    assert grid[0][0] == 2
    assert grid[0][2] == 2
    assert grid[3][2] == 0
    assert grid[4][2] == 0
    assert grid[2][0] == 1
