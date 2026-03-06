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

if __name__ == "__main__":
    x = 2
    y = 3
    z = sum(x,y)
    print(f"{x} + {y} = {z}")