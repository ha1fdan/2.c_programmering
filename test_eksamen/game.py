import pygame as pg
import random
import time
screen = pg.display.set_mode((400,400))
running = True
x = 100
y = 200
colors = [(255,0,0),(0,255,0),(0,0,255)]
currentColor=0
while running:
    events = pg.event.get()
    for e in events:
        
        if e.type == pg.QUIT:
            running = False
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                running = False
            if e.key == pg.K_SPACE:
                currentColor+=1
                if currentColor > len(colors)-1:
                    currentColor=0
  
    x += 5
    if x > 400:
        x = 0

    screen.fill((0,0,0))
    pg.draw.circle(screen, colors[currentColor], (x, y), 50) # skift (200,0,0) til (0,0,255) da, rgb
     
    pg.display.update()
    time.sleep(0.01)
