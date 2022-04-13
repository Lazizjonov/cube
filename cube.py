# This code is written by Lazizjonov Jasurbek
# 12.04.2022 Tashkent, Uzbekistan.

# Implementation of Rubick's Cube (RC) with python turtle
# To date I developed view of RC and made some refresh function to clean screen and redraw RC (with different angles) from different views




from time import sleep
import turtle
import math

rad = math.radians

# redefining sinus and cosinus functions to use in light form
def sin(x):
    return math.sin(rad(x))

def cos(x):
    return math.cos(rad(x))

pi = math.pi
colors = ["white", "red", "blue", "orange", "green", "yellow"]


# turtle.tracer(0, 0) is used to make the speed of turtle object as fast as possible
# it is used with turtle.update() function at the end of movement to display changes.

# turtle.tracer(0, 0)
t = turtle.getturtle()
t.hideturtle()
t.speed(0)
xAxis = 315
yAxis = 90
zAxis = 225
clen = 40

def setPoint(xpos, ypos, zpos, xa = xAxis, ya = yAxis, za = zAxis):
    y = ypos*sin(ya) + xpos*sin(xa) + zpos*sin(za)
    x = ypos*cos(ya) + xpos*cos(xa) + zpos*cos(za)
    # t.setpos(x,y)
    return (x,y)


class Rect:
    def __init__(self, color):
        self.p1 = (0,0)
        self.p2 = (0,0)
        self.p3 = (0,0)
        self.p4 = (0,0)
        self.color = color

class Cube:
    def __init__(self, xSide=0, ySide=0, zSide=0, mxSide=0, mySide=0, mzSide=0, xPos=0, yPos=0, zPos=0):
        self.xSide, self.ySide, self.zSide, self.mxSide, self.mySide, self.mzSide = ySide, zSide, mxSide, mySide, mzSide, xSide
        self.sides = [self.xSide, self.ySide, self.zSide, self.mxSide, self.mySide, self.mzSide]
        self.xPos = xPos
        self.yPos = yPos
        self.zPos = zPos

class rubics:
    def __init__(self, xPos, yPos):
        self.xPos, self.yPos = xPos, yPos
    
    cubes = []
    for i in range(3):
        cubes.append([])
        for j in range(3):
            cubes[i].append([])
            for k in range(3):
                cubes[i][j].append([])
                cubes[i][j][k] = Cube(
                    xPos=(1.5-j)*(clen+2), 
                    yPos=(1.5-i)*(clen+2), 
                    zPos=(1.5-k)*(clen+2))

    for i in range(3):
        for j in range(3):
            for k in range(3):
                if i==0:
                    cubes[i][j][k].ySide = Rect(color="white")
                if j==0:
                    cubes[i][j][k].xSide = Rect(color="blue")
                if k==0:
                    cubes[i][j][k].zSide = Rect(color="red")
                if j==2:
                    cubes[i][j][k].mxSide = Rect(color="green")
                if k==2:
                    cubes[i][j][k].mzSide = Rect(color="orange")
                if i==2:
                    cubes[i][j][k].mySide = Rect(color="yellow")
                if i==1:
                    cubes[i-1][j][k].myside = cubes[i][j][k]
                    cubes[i][j][k].ySide = cubes[i-1][j][k]
                    cubes[i][j][k].mySide = cubes[i+1][j][k]
                    cubes[i+1][j][k].ySide = cubes[i][j][k]
                if j==1:
                    cubes[i][j-1][k].mxSide = cubes[i][j][k]
                    cubes[i][j][k].xSide = cubes[i][j-1][k]
                    cubes[i][j+1][k].xSide = cubes[i][j][k]
                    cubes[i][j][k].mxSide = cubes[i][j+1][k]
                if k==1:
                    cubes[i][j][k-1].mzSide = cubes[i][j][k]
                    cubes[i][j][k].zSide = cubes[i][j][k-1]
                    cubes[i][j][k+1].zSide = cubes[i][j][k]
                    cubes[i][j][k].mzSide = cubes[i][j][k+1]
        


rub = rubics(0, 0)
if(rub.cubes[1][1][1].xSide == rub.cubes[1][0][1]):
    print("yse")


s = t.getscreen()
s.bgcolor("silver")


t.penup()
t.pencolor('black')

# setPoints() function sets points of a single cube which is passed as first argument in the position xp, yp, zp
# 3 default arguments are x,y,z axis on 3d implemented in 2d

def setPoints(c, xp, yp, zp, xa = xAxis, ya = yAxis, za = zAxis):
    arg = (xa, ya, za)
    if hasattr(c.xSide, "color"):
        c.xSide.p1 = setPoint(xp, yp, zp, *(arg))
        c.xSide.p2 = setPoint(xp, yp - clen, zp, *(arg))
        c.xSide.p3 = setPoint(xp, yp - clen, zp - clen, *(arg))
        c.xSide.p4 = setPoint(xp, yp, zp - clen, *(arg))
    if hasattr(c.ySide, "color"):
        c.ySide.p1 = setPoint(xp, yp, zp, *(arg))
        c.ySide.p2 = setPoint(xp - clen, yp, zp, *(arg))
        c.ySide.p3 = setPoint(xp - clen, yp, zp - clen, *(arg))
        c.ySide.p4 = setPoint(xp, yp, zp - clen, *(arg))
    if hasattr(c.zSide, "color"):
        c.zSide.p1 = setPoint(xp, yp, zp, *(arg))
        c.zSide.p2 = setPoint(xp, yp - clen, zp, *(arg))
        c.zSide.p3 = setPoint(xp - clen, yp - clen, zp, *(arg))
        c.zSide.p4 = setPoint(xp - clen, yp, zp, *(arg))
    if hasattr(c.mxSide, "color"):
        c.mxSide.p1 = setPoint(xp - clen, yp, zp, *(arg))
        c.mxSide.p2 = setPoint(xp - clen, yp, zp - clen, *(arg))
        c.mxSide.p3 = setPoint(xp - clen, yp - clen, zp - clen, *(arg))
        c.mxSide.p4 = setPoint(xp - clen, yp - clen, zp, *(arg))
    if hasattr(c.mySide, "color"):
        c.mySide.p1 = setPoint(xp, yp - clen, zp, *(arg))
        c.mySide.p2 = setPoint(xp - clen, yp - clen, zp, *(arg))
        c.mySide.p3 = setPoint(xp - clen, yp - clen, zp - clen, *(arg))
        c.mySide.p4 = setPoint(xp, yp - clen, zp - clen, *(arg))
    if hasattr(c.mzSide, "color"):
        c.mzSide.p1 = setPoint(xp, yp, zp - clen, *(arg))
        c.mzSide.p2 = setPoint(xp, yp - clen, zp - clen, *(arg))
        c.mzSide.p3 = setPoint(xp - clen, yp - clen, zp - clen, *(arg))
        c.mzSide.p4 = setPoint(xp - clen, yp, zp - clen, *(arg))

# Function to draw rectangle side of a single cube
def drawRect(recSide):
    t.fillcolor(recSide.color)
    t.setpos(recSide.p1)
    t.begin_fill()
    t.setpos(recSide.p2)
    t.setpos(recSide.p3)
    t.setpos(recSide.p4)
    t.setpos(recSide.p1)
    t.end_fill()

# Function to draw a single cube
# It calls drawRect function 6 times to draw all six sides (rectangles) of cube
# todo: rectangles should be drawn only if they are faced to screen else not 
def drawCube(c):
    if hasattr(c.xSide, "color") and xAxis < 360 and xAxis > 180:
        drawRect(c.xSide)
    if hasattr(c.ySide, "color"):
        drawRect(c.ySide)
    if hasattr(c.zSide, "color") and zAxis < 360 and zAxis > 180:
        drawRect(c.zSide)
    if hasattr(c.mxSide, "color") and xAxis < 180:
        drawRect(c.mxSide)
    if hasattr(c.mySide, "color"):
        drawRect(c.mySide)
    if hasattr(c.mzSide, "color") and zAxis < 180:
        drawRect(c.mzSide)

# drawCube2(rub.cubes[2][2][2], 0, 0, 0)

def refresh():
    t.clear()
    for i in range(3):
        for j in range(3):
            for k in range(3):
                t.penup()
                setPoints(rub.cubes[i][j][k], (1.5-j)*(clen+2), (1.5-i)*(clen+2), (1.5-k)*(clen+2))
                drawCube(rub.cubes[i][j][k])
    turtle.update()
    sleep(0.2)

for i in range(3):
    for j in range(3):
        for k in range(3):
            t.penup()
            setPoints(rub.cubes[i][j][k], (1.5-j)*(clen+2), (1.5-i)*(clen+2), (1.5-k)*(clen+2))
            drawCube(rub.cubes[i][j][k])

def clicked(point1, point2):
    global xAxis
    global zAxis
    for i in range(18):
        xAxis = (xAxis + 10) % 360
        zAxis = (zAxis + 10) % 360
        refresh()

# turtle.update()
# s.onclick(clicked)
# s._root.mainloop()
