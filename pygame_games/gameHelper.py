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
        self.bullet_angle = 0
        self.health = 100
    
    def moveWithKeys(self,):
        keys = pygame.key.get_pressed()
        bullet=None
        if keys[pygame.K_UP] and self.player_y - self.PLAYER_RADIUS > 0:
            self.player_y -= self.player_speed
            self.bullet_angle = -90
        if keys[pygame.K_DOWN] and self.player_y + self.PLAYER_RADIUS < self.SCREEN_HEIGHT:
            self.player_y += self.player_speed
            self.bullet_angle = 90
        if keys[pygame.K_LEFT] and self.player_x - self.PLAYER_RADIUS > 0:
            self.player_x -= self.player_speed
            self.bullet_angle = 180
        if keys[pygame.K_RIGHT] and self.player_x + self.PLAYER_RADIUS < self.SCREEN_WIDTH:
            self.player_x += self.player_speed
            self.bullet_angle = 0
        if keys[pygame.K_SPACE]:
            bullet = Bullet(
                self.SCREEN_WIDTH,
                self.SCREEN_HEIGHT,
                5,
                self.player_x,
                self.player_y,
                self.bullet_angle
            )

        return self.player_x, self.player_y, bullet
    
    def updatePostion(self,gameScreen, color: tuple):
        # update player postion on screen
        pygame.draw.circle(gameScreen, color, (self.player_x, self.player_y), self.PLAYER_RADIUS)
        
    
class Bullet():
    def __init__(self, screen_width, screen_height, bullet_radius, shooter_x, shooter_y, bullet_angle):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bullet_radius = bullet_radius
        self.bullet_x = shooter_x
        self.bullet_y = shooter_y
        self.bullet_angle = bullet_angle
        self.bullet_speed = 10

        # spawn slightly outside player
        angle_rad = math.radians(self.bullet_angle)
        self.bullet_x += math.cos(angle_rad) * 30
        self.bullet_y += math.sin(angle_rad) * 30

    def move(self):
        angle_rad = math.radians(self.bullet_angle)
        self.bullet_x += math.cos(angle_rad) * self.bullet_speed
        self.bullet_y += math.sin(angle_rad) * self.bullet_speed

    def updatePostion(self, gameScreen, color: tuple):
        pygame.draw.circle(gameScreen, color, (int(self.bullet_x), int(self.bullet_y)), self.bullet_radius)

    def offScreen(self):
        return (
            self.bullet_x < 0 or
            self.bullet_x > self.screen_width or
            self.bullet_y < 0 or
            self.bullet_y > self.screen_height
        )

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