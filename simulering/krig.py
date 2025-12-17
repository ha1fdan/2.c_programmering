import random
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


"""Lav et deck der er blandet med 52 kort. Til 2 spillere, så hver spiller får 26 kort."""
deck_cards=[]
for card in range(1,53):
    deck_cards.append(card)
random.shuffle(deck_cards)
player1_cards = deck_cards[:26]
player2_cards = deck_cards[26:]

def spilKrig(spiller1_kort_bunke, spiller2_kort_bunke):
    """I krig, skal hver spiller trække 3 kort og så vælge et af de kort til at sammenligne. Den med det højeste kort vinder alle kortene."""
    if len(spiller1_kort_bunke) < 4 or len(spiller2_kort_bunke) < 4:
        logger.warning("En af spillerne har ikke nok kort til at fortsætte krigen.")
        return

    spiller1_krig_kort = []
    spiller2_krig_kort = []
    
    for _ in range(3):
        spiller1_krig_kort.append(spiller1_kort_bunke.pop(0))
        spiller2_krig_kort.append(spiller2_kort_bunke.pop(0))
    
    # vælg et tilfældigt kort fra de 3 kort
    spiller1_krig_kort_valgt = random.choice(spiller1_krig_kort)
    spiller2_krig_kort_valgt = random.choice(spiller2_krig_kort)
    
    if spiller1_krig_kort_valgt > spiller2_krig_kort_valgt:
        spiller1_kort_bunke.extend(spiller1_krig_kort + spiller2_krig_kort)
    elif spiller2_krig_kort_valgt > spiller1_krig_kort_valgt:
        spiller2_kort_bunke.extend(spiller1_krig_kort + spiller2_krig_kort)
    else:
        logger.info(f"Spillerne har begge trukket: {spiller1_krig_kort_valgt} og {spiller2_krig_kort_valgt}. Krig igen!")
        spiller1_kort_bunke, spiller2_kort_bunke = spilKrig(spiller1_kort_bunke, spiller2_kort_bunke)
    
    return spiller1_kort_bunke, spiller2_kort_bunke
    

def nyRunde(spiller1_kort_bunke, spiller2_kort_bunke) -> tuple[list[int], list[int]]:
    """Spiller en runde krig mellem to spillere."""
    
    if not spiller1_kort_bunke or not spiller2_kort_bunke:
        logger.warning("En af spillerne har ingen kort tilbage.")
        return spiller1_kort_bunke, spiller2_kort_bunke

    kort1 = spiller1_kort_bunke.pop(0)
    kort2 = spiller2_kort_bunke.pop(0)
    
    logger.debug(f"Spiller 1 trækker: {kort1}, Spiller 2 trækker: {kort2}")

    if kort1 > kort2:
        spiller1_kort_bunke.extend([kort1, kort2])
    elif kort2 > kort1:
        spiller2_kort_bunke.extend([kort2, kort1])
    elif kort1 == kort2:
        logger.debug("Uafgjort! Så er der Krig!")
        spiller1_kort_bunke, spiller2_kort_bunke = spilKrig(spiller1_kort_bunke, spiller2_kort_bunke)

    return spiller1_kort_bunke, spiller2_kort_bunke


if __name__ == "__main__":
    runder = 0
    while player1_cards and player2_cards:
        player1_cards, player2_cards = nyRunde(player1_cards, player2_cards)
        runder += 1
        # da jeg normalt spiller med at man blander kortne efter hvber runde, så gør jeg det her også
        random.shuffle(player1_cards)
        random.shuffle(player2_cards)

    if player1_cards:
        print(f"Spiller 1 vinder efter {runder} runder!")
    else:
        print(f"Spiller 2 vinder efter {runder} runder!")