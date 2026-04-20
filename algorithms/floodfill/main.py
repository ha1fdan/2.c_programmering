#! /usr/bin/env python3
# Left click to draw black
# Right click to fill with the selected color
import pygame as pg
import time

def currentTime():
    return str(int(round(time.time() * 1000, 5)))[::3]

from floodfill import floodfill


def reset_grid(height, width):
    grid = [[1] * width for _ in range(height)]
    for row in range(height):
        grid[row][width // 2] = 0
    for col in range(width):
        grid[height // 2][col] = 0
    return grid

# Setup pygame
h = 42
w = 42
px_size = 20
fps = 60

pg.init()
screen = pg.display.set_mode((w*px_size, h*px_size))
clock = pg.time.Clock()


image = reset_grid(h, w)
        
        

left_pressed = False
fill_color = (0,0,200)
eraser_pressed = False
needs_redraw = True

BLACK = (0, 0, 0)
EMPTY = (200, 200, 200)

running = True
while running:
 
    for event in pg.event.get():
        if event.type == pg.QUIT:
            # Close window
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_1:
                fill_color = (0,0,200)
                needs_redraw = True
            elif event.key == pg.K_2:
                fill_color = (200,0,0)
                needs_redraw = True
            elif event.key == pg.K_3:
                fill_color = (0,200,0)
                needs_redraw = True
            elif event.key == pg.K_s:
                pg.image.save(screen, f"drawing_{currentTime()}.png")
            elif event.key == pg.K_q:
                image = reset_grid(h, w)
                needs_redraw = True
            
            
        ### Eraser
            if event.key == pg.K_e:
                eraser_pressed = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_e:
                eraser_pressed = False
            

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                left_pressed = True
            
            if event.button == 3:
                x, y = event.pos
                row = y//px_size
                col = x//px_size
                if 0 <= row < h and 0 <= col < w:
                    floodfill(image,row,col,fill_color)
                    needs_redraw = True

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                left_pressed = False

    if left_pressed:
        x,y = pg.mouse.get_pos()
        row = y//px_size
        col = x//px_size
        if 0 <= row < h and 0 <= col < w and image[row][col] != 0:
            image[row][col] = 0
            needs_redraw = True
    
    if eraser_pressed:
        x,y = pg.mouse.get_pos()
        row = y//px_size
        col = x//px_size
        if 0 <= row < h and 0 <= col < w and image[row][col] != 1:
            image[row][col] = 1
            needs_redraw = True

    if needs_redraw:
        screen.fill(BLACK)
        for row in range(h):
            for col in range(w):
                if image[row][col] == 0:
                    color = BLACK
                elif image[row][col] == 1:
                    color = EMPTY
                else:
                    color = image[row][col]

                pg.draw.rect(
                    screen,
                    color,
                    (col*px_size+1, row*px_size+1, px_size-1, px_size-1)
                )

        pg.display.flip()
        needs_redraw = False

    clock.tick(fps)

pg.quit()