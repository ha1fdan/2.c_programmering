import pygame as pg
import time
from math import cos, pi, sin

from helper import draw_grid, line_segments_intersection, cramers_rule, linepeace_with_parm_s

pg.init()

w = 800
h = 600 
screen = pg.display.set_mode((w, h))
font = pg.font.Font(None, 40) # Default font

p1 = [100,100]
p2 = [300, 300]
p3 = [500, 500]
p4 = [500, 200]

running = True
while running:

    ## Events ##
    events = pg.event.get()
    for e in events:
        if e.type == pg.QUIT:
            running = False
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                running = False        

        elif e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                p1 = e.pos
            if e.button == 3:
                p2 = e.pos

    ## Logic / Updates ##
    interaction = line_segments_intersection(p1,p2,p3,p4)
    if interaction[0]:
        text = font.render(f"Line segments intersect! At: {interaction[1]}", True, (50,50,50))
    else:
        text = font.render("Line segments do not intersect!", True, (50,50,50))

    ## Drawing ##
    screen.fill((240,240,240))
    draw_grid(screen, (150,150,150), 20)

    pg.draw.line(screen, (10,10,10), p1, p2, 4)
    pg.draw.circle(screen, (220,40,40), p1,6)
    pg.draw.circle(screen, (220,40,40), p2,6)

    pg.draw.line(screen, (10,10,10), p3, p4, 4)
    pg.draw.circle(screen, (40,40,220), p3,6)
    pg.draw.circle(screen, (40,40,220), p4,6)

    screen.blit(text, [20,20])

    pg.display.update()

    time.sleep(0.01)

pg.quit()
