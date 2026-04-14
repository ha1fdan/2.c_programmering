from floodfill import floodfill

def test_ff_full_boundaries():
    grid = [[1,1,1],
            [1,0,1],
            [1,1,1]]

    expected = [[1,1,1],
                [1,2,1],
                [1,1,1]]

    floodfill(grid,1,1,2)

    assert grid == expected

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

        