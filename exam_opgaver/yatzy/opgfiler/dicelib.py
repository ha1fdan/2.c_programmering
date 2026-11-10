import random

def roll(n):

    # Roll n dice and return the rolls as a list
    rolls = []
    for _ in range(n):
        r = random.randint(1,6)
        rolls.append(r)

    return rolls


def count(k, rolls):

    # Count the number of times the roll k
    # is among the rolls.
    #
    # count(3, [3,2,3,5,6]) returns 2
    n = 0
    for r in rolls:
        if r == k:
            n += 1
    return n


def large_straight(rolls):
    n = len(rolls)
    for i in range(1, n+1):
        if i not in rolls:
            return False
    return True
