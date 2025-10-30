import pygame
import sys
import gameHelper

# Colors
redColor = (200, 0, 0)
greenColor = (0, 200, 0)
blueColor = (0, 0, 200)

# Init
pygame.init()
WIDTH, HEIGHT = 600, 400
myGame = gameHelper.Game(WIDTH, HEIGHT)

# Player
myPlayer = gameHelper.Player(WIDTH, HEIGHT, 20)

# Enemys
enemys = []
for _ in range(10):
    enemys.append(gameHelper.Enemy(WIDTH, HEIGHT, 15))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move player
    player_x, player_y, bullet = myPlayer.moveWithKeys()

    # Draw background and player
    myGame.gameScreen.fill((30,30,30))
    myPlayer.updatePostion(myGame.gameScreen, greenColor)
    
    for enemy in enemys:
        enemy_x, enemy_y = enemy.moveTowardsPlayer(player_x, player_y)
        enemy.updatePostion(myGame.gameScreen, redColor)
    
    if bullet:
        bullet.updatePostion(myGame.gameScreen, blueColor)
    # Draw circle in each opposite corner (right bottom and left top)
    #pygame.draw.circle(myGame.gameScreen, (200, 0, 0), (WIDTH - player_radius, HEIGHT - player_radius), 50)
    #pygame.draw.circle(myGame.gameScreen, (200, 0, 0), (player_radius, player_radius), 50)
    
    

    pygame.display.flip()
    myGame.clock.tick(60)