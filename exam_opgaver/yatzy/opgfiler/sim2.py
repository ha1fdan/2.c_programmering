from dicelib import roll, count

N = 100000


def two_pairs(dice):
    return sum(count(f, dice) == 2 for f in range(1, 7)) == 2


def yatzy_round():
    dice = roll(5)
    for _ in range(2):
        face = max(range(1, 7), key=lambda f: count(f, dice))
        keep = count(face, dice)
        if keep == 5:
            break
        dice = [face] * keep + roll(5 - keep)
    return dice


print(f"To par: {sum(two_pairs(roll(5)) for _ in range(N)) / N * 100:.2f}%")
print(f"Fem ens (Yatzy) med 3 kast og låsning: "
      f"{sum(count(d[0], d) == 5 for d in (yatzy_round() for _ in range(N))) / N * 100:.2f}%")
