import pygame as pg
import math
from typing import Optional

def draw_grid(screen, line_color, grid_size):
    w, h = screen.get_size()
    for x in range(0, w, grid_size):
        pg.draw.line(screen, line_color, (x,0), (x,h), 1)
    for y in range(0, h, grid_size):
        pg.draw.line(screen, line_color, (0,y), (w,y), 1)
        

def cramers_rule(a1: float, b1: float, c1: float, a2: float, b2: float, c2: float) -> tuple[float, float]:
    """
    a1*x+b1*y=c1
    a2*x+b2*y=c2
    
    
    x=(c1*b2-c2*b1)/(a1*b2-a2*b1)
    y=(a1*c2-a2*c1)/(a1*b2-a2*b1)
    """
    
    det = a1 * b2 - a2 * b1
    if abs(det) < 1e-12:
        raise ValueError("ingen unik løsning")
    x = (c1 * b2 - c2 * b1) / det
    y = (a1 * c2 - a2 * c1) / det
    return x, y


def linepeace_with_parm_s(x1: float, y1: float, x2: float, y2: float, s: float) -> tuple[float, float]:
    """
    A=(x_1,y_1)
    B=(x_2,y_2)
    
    P = (x_1+s * (x_2-x_1), y_1+s * (y_2-y_1))
    """
    px = x1 + s * (x2 - x1)
    py = y1 + s * (y2 - y1)
    return px, py


# collision detection between two line segments
def line_segments_intersection(A: tuple,B: tuple,C: tuple,D: tuple) -> tuple[bool, Optional[tuple[float,float]]]:
    """
    A=(x1,y1)
    B=(x2,y2)
    C=(x3,y3)
    D=(x4,y4)
    
    returns (True,(px,py)) hvis der skæres mellem AB and CD
    ellers returns (False,None)
    """
    x1,y1=A
    x2,y2=B
    x3,y3=C
    x4,y4=D
    
    a1=y2 - y1
    b1=x1 - x2
    c1=a1*x1 + b1*y1
    
    a2=y4 - y3
    b2=x3 - x4
    c2=a2*x3 + b2*y3
    
    try:
        px,py=cramers_rule(a1,b1,c1,a2,b2,c2)
    except ValueError:
        return False,None # der er ingen skæring mellem de 2 linjer
    
    # tjek om P er mellem AB and CD
    def is_between(p: float, q: float, r: float) -> bool:
        return min(p, r) <= q <= max(p, r)
    
    if is_between(x1, px, x2) and is_between(y1, py, y2) and is_between(x3, px, x4) and is_between(y3, py, y4):
        return True,(round(px,3),round(py, 3))
    else:
        return False,None