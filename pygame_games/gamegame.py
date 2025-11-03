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
for _ in range(15):
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
    
    
    # Check collisions between player and enemys
    for enemy in enemys:
        dist_x = enemy.enemy_x - player_x
        dist_y = enemy.enemy_y - player_y
        distance = (dist_x ** 2 + dist_y ** 2) ** 0.5
        if distance < myPlayer.PLAYER_RADIUS + enemy.ENEMY_RADIUS:
            # Collision detected, reduce health
            myPlayer.health -= 1
            if myPlayer.health < 0:
                myPlayer.health = 0
                
    # Check collisions between bullet and enemys
    if bullet:
        for enemy in enemys:
            dist_x = enemy.enemy_x - bullet.bullet_x
            dist_y = enemy.enemy_y - bullet.bullet_y
            distance = (dist_x ** 2 + dist_y ** 2) ** 0.5
            if distance < bullet.bullet_radius + enemy.ENEMY_RADIUS:
                # Collision detected, remove enemy
                enemys.remove(enemy)
                break  # Exit loop to avoid modifying list during iteration
    
    
    # Draw score at top left
    font = pygame.font.Font(None, 24)
    text = font.render(f"Health: {myPlayer.health:03d}", True, (255, 255, 255))
    myGame.gameScreen.blit(text, (10, 10))

    # Update screen
    pygame.display.flip()
    myGame.clock.tick(60)
    
    if myPlayer.health <= 0:
        print("Game Over!")
        pygame.quit()
        sys.exit()
    elif len(enemys) == 0:
        print("You Win!")
        pygame.quit()
        sys.exit()