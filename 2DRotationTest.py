import turtle
import math

def sin(x):
    return math.sin(math.radians(x))

def cos(x):
    return math.cos(math.radians(x))


t = turtle.getturtle()
px = 200
py = 100
t.penup()
t.setpos(px, py)
t.pendown()

def rotatePoint2D(cx, cy, alfa:float):
    cosine = math.cos(math.radians(alfa))
    sine = math.sin(math.radians(alfa))
    x = (px - cx)  * cosine - (py - cy) * sine
    y = (px - cx) * sine + (py - cy) * cosine
    return x + cx, y + cy

for i in range(20*360):
    px, py = rotatePoint2D(50, 150, 1)
    t.setpos(px, py)
