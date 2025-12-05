#!/bin/env python3
"""import random;N=1_000_000;s=sum(1 for _ in range(N) if random.randrange(3)==random.randrange(3));print(f"stay wins:   {s}/{N} = {s/N:.6f}");print(f"switch wins: {N-s}/{N} = {(N-s)/N:.6f}")"""

import random
N=1_000_000

def simulate(n: int) -> tuple[int, int]:
    wins_stay,wins_switch=0,0
    rand = random.randrange
    for _ in range(n):
        car,pick=rand(3),rand(3); 
        if pick == car: wins_stay += 1
        else: wins_switch += 1
    return wins_stay,wins_switch

stay_wins, switch_wins = simulate(N)
print(f"stay wins:   {stay_wins}/{N} = {stay_wins/N:.6f}")
print(f"switch wins: {switch_wins}/{N} = {switch_wins/N:.6f}")