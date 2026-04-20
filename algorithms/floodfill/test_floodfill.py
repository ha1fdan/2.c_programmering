from floodfill import floodfill
import pytest

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

    with pytest.raises(ValueError, match="Point already has the fill value"):
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


# Start i kanten af billedet uden crash
def test_ff_edge_start_no_crash():
    grid = [[0,0,0],
            [1,1,0],
            [0,0,0]]

    expected = [[3,3,3],
                [1,1,3],
                [3,3,3]]

    floodfill(grid, 0, 2, 3)

    assert grid == expected


# Tomt gitter håndteres uden crash
def test_ff_empty_grid_no_crash():
    grid = []

    with pytest.raises(ValueError, match="Grid cannot be empty"):
        floodfill(grid, 0, 0, 1)

    assert grid == []


# Start-række uden for billedet ændrer ikke gitteret
def test_ff_row_out_of_bounds_no_change():
    grid = [[0,0],
            [0,0]]

    expected = [[0,0],
                [0,0]]

    with pytest.raises(ValueError, match="Point is out of bounds"):
        floodfill(grid, 5, 0, 1)

    assert grid == expected


# Start-kolonne uden for billedet ændrer ikke gitteret
def test_ff_col_out_of_bounds_no_change():
    grid = [[0,0],
            [0,0]]

    expected = [[0,0],
                [0,0]]

    with pytest.raises(ValueError, match="Point is out of bounds"):
        floodfill(grid, 0, 5, 1)

    assert grid == expected


# Negativ startposition håndteres som uden for billede
def test_ff_negative_index_out_of_bounds_no_change():
    grid = [[0,0],
            [0,0]]

    expected = [[0,0],
                [0,0]]

    with pytest.raises(ValueError, match="Point is out of bounds"):
        floodfill(grid, -1, 0, 1)

    assert grid == expected


# Indviklet mønster: fyldning følger smalle korridorer uden at krydse vægge
def test_ff_intricate_pattern_corridors():
    grid = [[0,1,0,0,0,1,0],
            [0,1,0,1,0,1,0],
            [0,0,0,1,0,0,0],
            [1,1,0,1,1,1,0],
            [0,0,0,0,0,1,0]]

    expected = [[7,1,7,7,7,1,7],
                [7,1,7,1,7,1,7],
                [7,7,7,1,7,7,7],
                [1,1,7,1,1,1,7],
                [7,7,7,7,7,1,7]]

    floodfill(grid, 0, 0, 7)

    assert grid == expected
