import random
from dicelib import roll, count


num_trails = 10000
num_four_of_a_kind = 0
for _ in range(num_trails):

    rolls = roll(5)

    for i in range(1,7):
        n = count(i, rolls)

        if n == 4:
            num_four_of_a_kind += 1

prob = num_four_of_a_kind/num_trails * 100

print("Trails:", num_trails)
print("Four of a kind:", num_four_of_a_kind)
print(f"Probability: {prob:.2f}%")
print()
