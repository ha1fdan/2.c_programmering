import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


"""
Linjeelementer for differentialligningen dy/dx = x·y

Linjeelementer viser hældningen af løsningskurverne i hvert punkt (x, y).
I hvert punkt beregnes hældningen dy/dx = x·y, og der tegnes et lille
linjeelement med den hældning. På den måde kan man se, hvordan løsningskurverne
forløber uden at løse ligningen analytisk.

Domæne: -5 < x < 5 og -5 < y < 5
"""

# Lav arrays med x- og y-værdier fra -5 til 5 med skridt 1
x = np.arange(-10, 10, 0.5)
y = np.arange(-5, 5, 0.5)

# Lav et gitter: X og Y indeholder alle kombinationer af x- og y-værdier
# så vi kan beregne hældningen i hvert punkt på én gang (vektorisering)
X, Y = np.meshgrid(x, y)

# Beregn hældningskomponenterne i hvert gitterpunkt
# dy/dx = x·y  =>  dy = x·y,  dx = 1 (x er den uafhængige variabel)
dy = X * Y
dx = np.ones(dy.shape)

# Normaliser vektorerne (dx, dy) til enhedsvektorer så alle pile er lige lange.
# Uden normalisering ville pile med stor hældning blive meget længere end andre,
# hvilket gør linjeelementerne svært at aflæse.
norm = np.sqrt(dx**2 + dy**2)
dxu = dx / norm  # x-komponent af enhedsvektoren
dyu = dy / norm  # y-komponent af enhedsvektoren

# Tegn linjeelementerne med quiver (pil-plot)
plt.quiver(X, Y, dxu, dyu, color="purple", headwidth=0, headlength=0, headaxislength=0)

# Løs begyndelsesværdiproblemet y(0) = 2 numerisk og tegn løsningskurven
x0, y0 = 0, 2
sol = solve_ivp(lambda x, y: [x * y[0]], [-5, 5], [y0], dense_output=True)
x_plot = np.linspace(-5, 5, 500)
y_plot = sol.sol(x_plot)[0]
plt.plot(x_plot, y_plot, color="red", label=f"y({x0}) = {y0}")

plt.title("Linjeelementer for dy/dx = x·y")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.show()
