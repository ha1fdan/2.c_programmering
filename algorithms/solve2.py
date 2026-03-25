from math import sqrt
import pytest

def solve2(a,b,c,y=0):
    """ Solves ax^2 + bx + c = y

    The y parameter is optional and defaults to 0.

    Returns the solutions as a list.
    An empty list is returned when there is no solutions.

    Raises TypeError on invalid inputs.
    """
    try:
        d = b**2 - 4*a*(c-y)
    except TypeError:
        raise TypeError("Coefficients a, b, c and y-value must be integers or floats")
        
    if d < 0:
        return []
    elif d == 0:
        x = (-b + sqrt(d))/(2*a)
        return [x]
    elif d > 0:
        x1 = (-b + sqrt(d))/(2*a)
        x2 = (-b - sqrt(d))/(2*a)
        return [x1, x2]
        
def test_solve2_invalid_a():
    with pytest.raises(TypeError, match="must be integers or floats"):
        solve2("1", 2, 3, 4)




if __name__ == "__main__":
    print("solve2 return", solve2(1,2,-6,2))
    print("solve2 TypeError", solve2("1",2,-6,2))
