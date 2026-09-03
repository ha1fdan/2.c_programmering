import pygame as pg
import time
import random
import sqlite3
con = sqlite3.connect("reaction-game.db")
con.row_factory = sqlite3.Row
pg.init()
w = 800
h = 800
screen = pg.display.set_mode((w,h))

font_large = pg.font.Font(None, 80)
font = pg.font.Font(None, 40)

clock = pg.time.Clock()

timer_start = None
wait_start = None
wait_duration = None

## Database setup
con.execute("CREATE TABLE IF NOT EXISTS highscores (id INTEGER PRIMARY KEY, name TEXT, reaction_time_ms REAL);")

name = ""
score_saved = False

state = "ready"
running = True
while running:
    
    events = pg.event.get() 
    for event in events:
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False


    if state == "ready":
        text = font_large.render(f"REACTION TIME", True, (255,255,255))
        text_rect = text.get_rect(center=(w/2, 100))
        screen.blit(text, text_rect)

        msgs = ["Press any key as fast as you can",
                "when the screen turns green!",
                "Press [space] to start the game"]
        for i, msg in enumerate(msgs):
            text = font.render(msg, True, (255,255,255))
            text_rect = text.get_rect(center=(w/2, h/2+i*100))
            screen.blit(text, text_rect)

        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    name = ""
                    score_saved = False
                    state = "wait"
                    wait_start = time.time()
                    wait_duration = random.uniform(2,5)


    elif state == "wait":
        screen.fill((0,0,0))

        if time.time() - wait_start > wait_duration:
            start_time = time.time()
            state = "timer"

        for event in events:
            if event.type == pg.KEYDOWN:
                state = "gameover"

        
    elif state == "gameover":
        screen.fill((200,20,20))

        text = font_large.render("GAME OVER!", True, (255,255,255))
        text_rect = text.get_rect(center=(w/2, h/2))
        screen.blit(text, text_rect)
        

    elif state == "timer":
        screen.fill((20,200,20))
        for event in events:
            if event.type == pg.KEYDOWN:
                state = "result"
                end_time = time.time()


    elif state == "result":
        reaction_time_ms = (end_time - start_time)*1000
        text = font.render(f"Your reaction time was: {reaction_time_ms:.1f} ms", True, (255,255,255))
        text_rect = text.get_rect(center=(w/2, 100))
        screen.blit(text, text_rect)

        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if not score_saved:
                        con.execute("INSERT INTO highscores (name, reaction_time_ms) VALUES (?, ?)", (name, reaction_time_ms))
                        con.commit()
                        score_saved = True
                    state = "highscores"
                elif event.unicode and event.unicode.isprintable():
                    name += event.unicode
 
        text = font_large.render(f"Name: {name}", True, (255,255,255))
        screen.blit(text, (50,200))

        
        
    elif state == "highscores":
        screen.fill((0,0,0))
        scores = con.execute("SELECT name, reaction_time_ms FROM highscores GROUP BY name ORDER BY reaction_time_ms ASC LIMIT 10").fetchall()
        for i, s in enumerate(scores, start=1):
            text = font.render(f"#{i}  {s['name']}   {round(s['reaction_time_ms'], 3)}", True, (255,255,255))
            screen.blit(text, (100,i*100))

        

    pg.display.update() 
    clock.tick(100)
