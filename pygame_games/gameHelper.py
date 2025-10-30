import pygame
import math
from random import randint

def randomMovementInput():
    return randint(-2, 2), randint(-2, 2)

class Game():
    def __init__(self, SCREEN_WIDTH: int, SCREEN_HEIGHT: int,):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.gameScreen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

class Player():
    def __init__(self, SCREEN_WIDTH: int, SCREEN_HEIGHT: int, PLAYER_RADIUS: int,):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.PLAYER_RADIUS = PLAYER_RADIUS
        self.start_x = SCREEN_WIDTH // 4
        self.start_y = SCREEN_HEIGHT // 2
        self.player_x = self.start_x
        self.player_y = self.start_y
        self.player_speed = 5
    
    def moveWithKeys(self,):
        keys = pygame.key.get_pressed()
        bullet=None
        if keys[pygame.K_UP] and self.player_y - self.PLAYER_RADIUS > 0:
            self.player_y -= self.player_speed
        if keys[pygame.K_DOWN] and self.player_y + self.PLAYER_RADIUS < self.SCREEN_HEIGHT:
            self.player_y += self.player_speed
        if keys[pygame.K_LEFT] and self.player_x - self.PLAYER_RADIUS > 0:
            self.player_x -= self.player_speed
        if keys[pygame.K_RIGHT] and self.player_x + self.PLAYER_RADIUS < self.SCREEN_WIDTH:
            self.player_x += self.player_speed
        if keys[pygame.K_SPACE]:
            # shoot bullet by spawining a Bullet object
            bullet=Bullet(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, 5, self.player_x, self.player_y, math.pi/2, 10)

        return self.player_x, self.player_y, bullet
    
    def updatePostion(self,gameScreen, color: tuple):
        # update player postion on screen
        pygame.draw.circle(gameScreen, color, (self.player_x, self.player_y), self.PLAYER_RADIUS)
    
class Bullet():
    def __init__(self, SCREEN_WIDTH: int, SCREEN_HEIGHT: int, BULLET_RADIUS: int, SHOOTER_X: int, SHOOTER_Y: int, TARGET_X: int, TARGET_Y: int):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.BULLET_RADIUS = BULLET_RADIUS
        self.bullet_x = SHOOTER_X
        self.bullet_y = SHOOTER_Y
        # Calculate angle between shooter and target
        dx = TARGET_X - SHOOTER_X
        dy = TARGET_Y - SHOOTER_Y
        self.BULLET_ANGLE = math.atan2(dy, dx)
        self.BULLET_SPEED = 2
    
    def shoot(self,):
        # update bullet position based on angle and speed
        self.bullet_x += self.BULLET_SPEED * math.cos(self.BULLET_ANGLE)
        self.bullet_y += self.BULLET_SPEED * math.sin(self.BULLET_ANGLE)
        return self.bullet_x, self.bullet_y
    
    def updatePostion(self,gameScreen, color: tuple):
        # update bullet postion on screen
        pygame.draw.circle(gameScreen, color, (int(self.bullet_x), int(self.bullet_y)), self.BULLET_RADIUS)

class Enemy():
    def __init__(self, SCREEN_WIDTH: int, SCREEN_HEIGHT: int, ENEMY_RADIUS: int,):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.ENEMY_RADIUS = ENEMY_RADIUS
        self.enemy_x = randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - ENEMY_RADIUS)
        self.enemy_y = randint(ENEMY_RADIUS, SCREEN_HEIGHT - ENEMY_RADIUS)
        self.ENEMY_SPEED = 1
        
    def moveTowardsPlayer(self, PLAYER_X: int, PLAYER_Y: int,):
        # Get random movement offset
        randomInput_x, randomInput_y = randomMovementInput()
        
        # Calculate new position with base movement towards player
        if self.enemy_x < PLAYER_X:
            self.enemy_x += self.ENEMY_SPEED
        elif self.enemy_x > PLAYER_X:
            self.enemy_x -= self.ENEMY_SPEED
        if self.enemy_y < PLAYER_Y:
            self.enemy_y += self.ENEMY_SPEED
        elif self.enemy_y > PLAYER_Y:
            self.enemy_y -= self.ENEMY_SPEED

        # Apply random movement while keeping enemy within screen bounds
        new_x = max(self.ENEMY_RADIUS, min(self.enemy_x + randomInput_x, self.SCREEN_WIDTH - self.ENEMY_RADIUS))
        new_y = max(self.ENEMY_RADIUS, min(self.enemy_y + randomInput_y, self.SCREEN_HEIGHT - self.ENEMY_RADIUS))
        
        self.enemy_x = new_x
        self.enemy_y = new_y
        
        return self.enemy_x, self.enemy_y
    
    def updatePostion(self,gameScreen, color: tuple):
        # update enemy postion on screen
        pygame.draw.circle(gameScreen, color, (self.enemy_x, self.enemy_y), self.ENEMY_RADIUS)