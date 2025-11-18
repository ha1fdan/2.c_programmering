import random
import sys

try:
    n_dice, n_sides = sys.argv[1].split("d")
except IndexError:
    n_dice = 1
    n_sides = 6

for i in range(int(n_dice)):
    print(random.randint(1,int(n_sides)))
