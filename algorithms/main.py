#!/usr/bin/env python3
from lib import sum, findMax, findMin, sortTS

### ================== TESTING =================== ###

def test_sum():
    assert sum(2,2) == 4

def test_max():
    assert findMax([1,16,3,9,66,33,52,79]) == 79

def test_min():
    assert findMin([1,16,3,9,66,33,52,79]) == 1

def test_sort():
    assert sortTS([1,16,3,9,66,33,52,79]) == [1,3,9,16,33,52,66,79]

if __name__ == "__main__":
    minListe=[56,43,21,99,0,67]
    print(f"Min: {findMin(minListe)}")
    print(f"Max: {findMax(minListe)}")
    print(f"Sorted: {sortTS(minListe)}")