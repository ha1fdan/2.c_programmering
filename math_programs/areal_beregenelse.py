import numpy as np
import matplotlib.pyplot as plt

def approx_area(f, a, b, n, method="left"):
    xs = np.linspace(a, b, n+1)
    dx = (b - a) / n
    
    if method == "left":
        x_used = xs[:-1]
    elif method == "right":
        x_used = xs[1:]
    elif method == "mid":
        x_used = (xs[:-1] + xs[1:]) / 2
    else:
        raise ValueError("method must be 'left', 'right' or 'mid'")
    
    area = np.sum(f(x_used) * dx)
    
    # Plot
    plt.figure()
    X = np.linspace(a, b, 400)
    plt.plot(X, f(X))
    plt.bar(x_used, f(x_used), width=dx, alpha=0.3, align='edge')
    plt.title(f"{n} rektangler — {method} Riemann")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()
    
    return area

# funktionen f
f = lambda x: x**3

# OPGAVE A — 1 rektangel, bredde 4, højde f(2)
area_a = approx_area(f, 0, 4, 1, method="mid")
print("a) Areal ≈", area_a)

# OPGAVE B — 2 rektangler, bredde 2, højder f(1) og f(3)
area_b = approx_area(f, 0, 4, 2, method="mid")
print("b) Areal ≈", area_b)

# OPGAVE C — Excel-agtig generalisering: mange rektangler
area_c = approx_area(f, 0, 4, 1000, method="mid")
print("c) Areal med 1000 rektangler ≈", area_c)

# Det rigtige areal analytisk
A_exact = (4**4)/4  # ∫ x^3 dx = x^4/4
print("Eksakt areal =", A_exact)
