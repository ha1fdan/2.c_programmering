import random
forsoeg=10
tal_at_gaette=random.randint(1,100)
for _ in range(forsoeg):
	print(f"Du har {forsoeg} forsøg tilbage")
	try:
		gaet=int(input("Tal du gætter på: "))
	except ValueError:
		print("Det er ikke et tal, prøv igen")
		continue
	if gaet < tal_at_gaette:
		print("for lavt")
		forsoeg-=1
	if gaet > tal_at_gaette:
		print("for højt")
		forsoeg-=1
	if gaet == tal_at_gaette:
		print(f"Du gættede at tallet var {tal_at_gaette}! flot!!!")
		break

print("Tak fordi du spillede mit spil :)")