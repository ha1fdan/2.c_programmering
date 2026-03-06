#!/usr/bin/env python3

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


### ======================================== ###

testingListe = [1,16,3,9,66,33,52,79]
print(findMax(testingListe))
print(findMin(testingListe))
print(sortTS(testingListe))