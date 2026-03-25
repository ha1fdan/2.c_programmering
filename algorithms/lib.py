import math

### -------------- Hjælpefunktioner -------------- ###
def _validate_number(value: float, name: str) -> None:
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} skal være et tal")


def _validate_number_list(values: list[float], name: str) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} skal være en liste")
    if len(values) == 0:
        raise ValueError("Listen er tom")
    if not all(isinstance(x, (int, float)) for x in values):
        raise TypeError(f"Alle elementer i {name} skal være tal")

### -------------- Modul 1 -------------- ###
def sum(a,b) -> float:
    # Handle int, float, list, and string combinations
    # Both numbers (int/float)
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a + b
    # Both lists: concatenate
    if isinstance(a, list) and isinstance(b, list):
        return a + b
    # List and number
    if isinstance(a, list) and isinstance(b, (int, float)):
        if not all(isinstance(x, (int, float)) for x in a):
            raise TypeError("Alle elementer i listen skal være tal")
        return [x + b for x in a]
    if isinstance(b, list) and isinstance(a, (int, float)):
        if not all(isinstance(x, (int, float)) for x in b):
            raise TypeError("Alle elementer i listen skal være tal")
        return [a + x for x in b]
    # Both strings
    if isinstance(a, str) and isinstance(b, str):
        return a + b
    # String and number (not supported)
    if (isinstance(a, str) and isinstance(b, (int, float))) or (isinstance(b, str) and isinstance(a, (int, float))):
        raise TypeError("Kan ikke lægge tal og tekst sammen")
    # String and list (not supported)
    if (isinstance(a, str) and isinstance(b, list)) or (isinstance(b, str) and isinstance(a, list)):
        raise TypeError("Kan ikke lægge tekst og liste sammen")
    raise TypeError(f"Kan ikke lægge {type(a).__name__} og {type(b).__name__} sammen")

def findMax(sejListe: list[float]) -> float:
    _validate_number_list(sejListe, "sejListe")
    stoersteTal = sejListe[0]
    #print("star tal: ", stoersteTal)
    for talDerTejkkes in sejListe:
        #print(f"tejekker om {talDerTejkkes} er større end {stoersteTal}")
        if talDerTejkkes > stoersteTal:
            #print("det nye største tal: ", talDerTejkkes)
            stoersteTal = talDerTejkkes

    return stoersteTal

def findMin(sejListe: list[float]) -> float:
    _validate_number_list(sejListe, "sejListe")
    mindsteTal = sejListe[0]
    for talDerTejkkes in sejListe:
        if talDerTejkkes < mindsteTal:
            mindsteTal = talDerTejkkes

    return mindsteTal

def sortTS(sejListe: list[float]) -> list[float]:
    _validate_number_list(sejListe, "sejListe")
    sortedList=[]
    while len(sejListe):
        cMin = findMin(sejListe)
        sortedList.append(cMin)
        sejListe.remove(cMin)

    return sortedList

### -------------- Modul 2 -------------- ###
def solve2(a: float, b: float, c: float, d: float) -> list[float]:
    """
    som løser funktionen løser ligningen ax^2 + bx + c = d. Beregn d og brug den til at vurdere hvorvidt der skal returneres 0, 1 eller 2 løsninger. Løsningerne kan passende returneres i en liste (hvis listen er tom er der nul løsninger, hvis den indeholder ét element var der en løsning osv.)
    """
    _validate_number(a, "a")
    _validate_number(b, "b")
    _validate_number(c, "c")
    _validate_number(d, "d")
    if a == 0:
        raise ValueError("a må ikke være 0")

    d = b**2 - 4*a*(c-d)

    if d < 0:
        return []
    elif d == 0:
        return [-b/(2*a)]
    else:
        return [(-b + math.sqrt(d))/(2*a), (-b - math.sqrt(d))/(2*a)]

def find(L: list[float], k: float) -> int | None:
    # som finder positionen af elementet k i en liste L eller returnere None hvis det ikke findes i listen. find([7,8,3,9,2],3) skal returnere 2, fordi 3 står på plads 2 i listen.
    _validate_number_list(L, "L")
    _validate_number(k, "k")
    for i in range(len(L)):
        if L[i] == k:
            return i
    raise ValueError(f"Elementet {k} findes ikke i listen")

if __name__ == "__main__":
    x = 2
    y = 3
    z = sum(x,y)
    print(f"{x} + {y} = {z}")