from dicelib import roll, count

N = 100000
hits = {k: 0 for k in (2, 3, 4, 5)}

for _ in range(N):
    dice = roll(5)
    for face in range(1, 7):
        c = count(face, dice)
        if c in hits:
            hits[c] += 1

print("Forsøg:", N)
for k, h in hits.items():
    print(f"{k} ens: {h:6d}  ->  {h / N * 100:.2f}%")
