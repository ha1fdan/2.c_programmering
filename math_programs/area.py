import math
from matplotlib import pyplot as plt

# plot x,y axes
plt.axhline(0, color='black',linewidth=0.5, ls='--')
plt.axvline(0, color='black',linewidth=0.5, ls='--')
plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

area=0
a=int(input("a? "))
b=int(input("b? "))
n=int(input("n? "))
delta_x=(b-a)/n

def f(x):
    return x**3

x = a
while x < b:
    area += delta_x * f(x)
    plt.bar(x, f(x), width=delta_x, color='blue', edgecolor='black', alpha=0.5)
    x += delta_x

# plot continuous curve of f(x)
xs = [a + i*(b - a) / 1000 for i in range(1001)]
ys = [f(xi) for xi in xs]
plt.plot(xs, ys, color='red', linewidth=2)

print(area)
plt.show()