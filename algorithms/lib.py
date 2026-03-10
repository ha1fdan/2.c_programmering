import math

### -------------- Modul 1 -------------- ###
def sum(a,b):
    return a + b

def findMax(sejListe) -> int:
    stoersteTal = sejListe[0]
    for talDerTejkkes in sejListe:
        if talDerTejkkes > stoersteTal:
            stoersteTal = talDerTejkkes

    return stoersteTal

def findMin(sejListe) -> int:
    mindsteTal = sejListe[0]
    for talDerTejkkes in sejListe:
        if talDerTejkkes < mindsteTal:
            mindsteTal = talDerTejkkes

    return mindsteTal

def sortTS(sejListe) -> list:
    sortedList=[]
    
    while len(sejListe):
        cMin = findMin(sejListe)
        sortedList.append(cMin)
        sejListe.remove(cMin)

    return sortedList

### -------------- Modul 2 -------------- ###
def solve2(a,b,c,d):
    """
    som løser funktionen løser ligningen ax^2 + bx + c = d. Beregn d og brug den til at vurdere hvorvidt der skal returneres 0, 1 eller 2 løsninger. Løsningerne kan passende returneres i en liste (hvis listen er tom er der nul løsninger, hvis den indeholder ét element var der en løsning osv.)
    """
    d = b**2 - 4*a*(c-d)

    if d < 0:
        return []
    elif d == 0:
        return [-b/(2*a)]
    else:
        return [(-b + math.sqrt(d))/(2*a), (-b - math.sqrt(d))/(2*a)]

def find(L,k):
    # som finder positionen af elementet k i en liste L eller returnere None hvis det ikke findes i listen. find([7,8,3,9,2],3) skal returnere 2, fordi 3 står på plads 2 i listen.
    for i in range(len(L)):
        if L[i] == k:
            return i
    return None

if __name__ == "__main__":
    x = 2
    y = 3
    z = sum(x,y)
    print(f"{x} + {y} = {z}")