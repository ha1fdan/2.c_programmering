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
    pass

def nyRunde(spiller1_kort_bunke, spiller2_kort_bunke) -> tuple[list[int], list[int]]:
    """Spiller en runde krig mellem to spillere."""
    
    if not spiller1_kort_bunke or not spiller2_kort_bunke:
        logger.warning("En af spillerne har ingen kort tilbage.")
        return spiller1_kort_bunke, spiller2_kort_bunke

    kort1 = spiller1_kort_bunke.pop(0)
    kort2 = spiller2_kort_bunke.pop(0)

    if kort1 > kort2:
        spiller1_kort_bunke.extend([kort1, kort2])
    elif kort2 > kort1:
        spiller2_kort_bunke.extend([kort2, kort1])
    elif kort1 == kort2:
        logger.debug("Uafgjort! Krig!")
        spilKrig(spiller1_kort_bunke, spiller2_kort_bunke) # Håndter krig situation

    return spiller1_kort_bunke, spiller2_kort_bunke


if __name__ == "__main__":
    runder = 0
    while player1_cards and player2_cards:
        player1_cards, player2_cards = nyRunde(player1_cards, player2_cards)
        runder += 1

    if player1_cards:
        print(f"Spiller 1 vinder efter {runder} runder!")
    else:
        print(f"Spiller 2 vinder efter {runder} runder!")