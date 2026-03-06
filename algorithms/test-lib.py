from lib import sum

def test_sum():
    assert sum(2,2) == 4

def test_sum_negative():
    assert sum(-2,-2) == 0

    