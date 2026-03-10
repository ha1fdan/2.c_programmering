#!/usr/bin/env python3
from lib import sum, findMax, findMin, sortTS, solve2, find

### ================== TESTING =================== ###

def test_sum():
    assert sum(2,2) == 4
    
def test_sum2():
    assert sum(2.2,2.2) == 4.4

def test_max():
    assert findMax([1,16,3,9,66,33,52,79]) == 79

def test_max2():
    assert findMax([1,2.2,8.9,6,3.7,11.2]) == 11.2

def test_max3():
    assert findMax([1,2.0,-0.1,-3,7.2]) == 7.2

def test_max4():
    assert findMax([-3,-2,-5,-1,-7,-8]) == -1

def test_max5():
    assert findMax([3,3,3,3,3,3,3,3,3]) == 3
    
def test_max6():
    assert findMax("Hej med dig") == "m"

def test_max7():
    assert findMax((1,16,3,9,66,33,52,79)) == 79
    
def test_max8():
    assert findMax([]) == None

def test_min():
    assert findMin([1,16,3,9,66,33,52,79]) == 1
    
def test_min2():
    assert findMin([2,5,-3,1,0]) == -3

def test_sort():
    assert sortTS([1,16,3,9,66,33,52,79]) == [1,3,9,16,33,52,66,79]

def test_sort2():
    assert sortTS([2,5.5,-3,1,0]) == [-3, 0, 1, 2, 5.5]

def test_solve2():
    sol = solve2(1,2,-6,2)
    assert 2 in sol and -4 in sol
    
def test_find():
    assert find([7,8,3,9,2],3) == 2
def test_find_2():
    assert find([7,8,3,9,2],5) == None

if __name__ == "__main__":
    minListe=[0,43,21,99,56,67]
    print(f"Min: {findMin(minListe)}")
    print(f"Max: {findMax(minListe)}")
    print(f"Sorted: {sortTS(minListe)}")
    print(f"Solutions: {solve2(1,2,-6,2)}")