import math

e_vaerdi = math.erf(2) # Samme som EKSP(2) i Excel (Fejlfunktionen) / LibreOffice's ERF(2)

kvadrat_roten_af_pi = math.sqrt(math.pi) 

areal = kvadrat_roten_af_pi * e_vaerdi

"""
LibreOffice Calc:
=SQRT(PI()) * ERF(2)
giver det samme.
"""

print(f'A={areal:.9f}')
# 1.764162782
