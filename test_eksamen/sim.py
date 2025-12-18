# Programmet slår med en virtuelle terninger (1 til 6)  
# The program rolls a virtual dice (1 to 6)

import random

N = 100
amountOfSixesRolled=0
timesTwoSixesRolledAtSameTime=0
amountOfOddNumberedRolls=0

for i in range(N):
    roll1 = random.randint(1,6)
    roll2 = random.randint(1,6)
    if roll1 == 6:
        amountOfSixesRolled+=1
        
    if roll1/2 != int(roll1/2):
        amountOfOddNumberedRolls+=1
        
    if roll1 == 6 and roll2 == 6:
        timesTwoSixesRolledAtSameTime+=1
    
    print("Rolls", roll1, roll2)

print("Seksere slåt:", amountOfSixesRolled)
print("Ulige tal slået:", amountOfOddNumberedRolls)
print("Gange 2 seksere var slået samtidig", timesTwoSixesRolledAtSameTime)