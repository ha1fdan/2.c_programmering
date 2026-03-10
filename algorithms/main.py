#!/usr/bin/env python3
from lib import sum, findMax, findMin, sortTS, solve2, find

### ================== TESTING =================== ###

def test_sum():
    assert sum(2,2) == 4

def test_max():
    assert findMax([1,16,3,9,66,33,52,79]) == 79

def test_min():
    assert findMin([1,16,3,9,66,33,52,79]) == 1

def test_sort():
    assert sortTS([1,16,3,9,66,33,52,79]) == [1,3,9,16,33,52,66,79]
    
def test_solve2():
    sol = solve2(1,2,-6,2)
    assert 2 in sol and -4 in sol
    
def test_find():
    assert find([7,8,3,9,2],3) == 2
def test_find_2():
    assert find([7,8,3,9,2],5) == None

if __name__ == "__main__":
    minListe=[56,43,21,99,0,67]
    print(f"Min: {findMin(minListe)}")
    print(f"Max: {findMax(minListe)}")
    print(f"Sorted: {sortTS(minListe)}")
    print(f"Solutions: {solve2(1,2,-6,2)}")