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

turtle.tracer(0, 0)
t = turtle.getturtle()
t.hideturtle()
t.speed(0)
xAxis = 315
yAxis = 90
zAxis = 225
clen = 40


# setPoint3() function takes 3d point and returns its 2d transition given degrees of all 3 axes
def setPoint3D(xpos, ypos, zpos, xa = xAxis, ya = yAxis, za = zAxis):
    y = ypos*sin(ya) + xpos*sin(xa) + zpos*sin(za)
    x = ypos*cos(ya) + xpos*cos(xa) + zpos*cos(za)
    # t.setpos(x,y)
    return (x,y)

class Point:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def changePoint(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def takePoint2D(self, xa = xAxis, ya = yAxis, za = zAxis):
        return setPoint3D(self.x, self.y, self.z, xa, ya, za)


class Rect:
    def __init__(self, color):
        self.p1 = Point(0,0,0)
        self.p2 = Point(0,0,0)
        self.p3 = Point(0,0,0)
        self.p4 = Point(0,0,0)
        self.color = color
    
    def getCenter(self):
        return [ (self.p1.x + self.p3.x)/2, (self.p1.y + self.p3.y)/2, (self.p1.z + self.p3.z)/2 ]

    # calcAngles() implements calculation on vector from the center of cube (cx, cy, cz) to center of rect (myCenter) 
    # and returns vector to calculate if it is visible or not
    def calcAngles(self, cx, cy, cz):
        myCenter = self.getCenter()
        print(myCenter[0], cx, myCenter[1], cy, myCenter[2], cz)
        return myCenter[0] + cx >= 0 and myCenter[1] + cy >= 0 and myCenter[2] + cz >= 0


# Each cube has 6 sides some sides has attribute color others are linked to other 
# cube that is positioned exactly at that side. 
# This link is supposed to help during rotation of cube parts
class Cube:
    def __init__(self, xSide=0, ySide=0, zSide=0, mxSide=0, mySide=0, mzSide=0, xPos=0, yPos=0, zPos=0):
        self.xSide, self.ySide, self.zSide, self.mxSide, self.mySide, self.mzSide = ySide, zSide, mxSide, mySide, mzSide, xSide
        self.xPos = xPos
        self.yPos = yPos
        self.zPos = zPos

    def getAllSides(self):
        return (self.xSide, self.ySide, self.zSide, self.mxSide, self.mySide, self.mzSide) 

    def getCenter(self):
        return (self.xPos - clen/2, self.yPos - clen/2, self.zPos - clen/2)


# Rubick's cube contains 27 single cubes united in traditional form 3x3x3
# rubics object contains cubes matrix which is 3x3x3 size
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
                cubes[i][j][k] = Cube()

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

def setPoints(c, xp, yp, zp):
    if hasattr(c.xSide, "color"):
        c.xSide.p1.changePoint(xp, yp, zp)
        c.xSide.p2.changePoint(xp, yp - clen, zp)
        c.xSide.p3.changePoint(xp, yp - clen, zp - clen)
        c.xSide.p4.changePoint(xp, yp, zp - clen)
    if hasattr(c.ySide, "color"):
        c.ySide.p1.changePoint(xp, yp, zp)
        c.ySide.p2.changePoint(xp, yp, zp - clen)
        c.ySide.p3.changePoint(xp - clen, yp, zp - clen)
        c.ySide.p4.changePoint(xp - clen, yp, zp)
    if hasattr(c.zSide, "color"):
        c.zSide.p1.changePoint(xp, yp, zp)
        c.zSide.p2.changePoint(xp - clen, yp, zp)
        c.zSide.p3.changePoint(xp - clen, yp - clen, zp)
        c.zSide.p4.changePoint(xp, yp - clen, zp)
    if hasattr(c.mxSide, "color"):
        c.mxSide.p1.changePoint(xp - clen, yp, zp)
        c.mxSide.p2.changePoint(xp - clen, yp, zp - clen)
        c.mxSide.p3.changePoint(xp - clen, yp - clen, zp - clen)
        c.mxSide.p4.changePoint(xp - clen, yp - clen, zp)
    if hasattr(c.mySide, "color"):
        c.mySide.p1.changePoint(xp, yp - clen, zp)
        c.mySide.p2.changePoint(xp - clen, yp - clen, zp)
        c.mySide.p3.changePoint(xp - clen, yp - clen, zp - clen)
        c.mySide.p4.changePoint(xp, yp - clen, zp - clen)
    if hasattr(c.mzSide, "color"):
        c.mzSide.p1.changePoint(xp, yp, zp - clen)
        c.mzSide.p2.changePoint(xp, yp - clen, zp - clen)
        c.mzSide.p3.changePoint(xp - clen, yp - clen, zp - clen)
        c.mzSide.p4.changePoint(xp - clen, yp, zp - clen)



# Function to draw rectangle side of a single cube
def drawRect(recSide):
    t.fillcolor(recSide.color)
    t.setpos(recSide.p1.takePoint2D())
    t.begin_fill()
    t.setpos(recSide.p2.takePoint2D())
    t.setpos(recSide.p3.takePoint2D())
    t.setpos(recSide.p4.takePoint2D())
    t.setpos(recSide.p1.takePoint2D())
    t.end_fill()

# Function to draw a single cube
# It calls drawRect function 6 times to draw all six sides (rectangles) of cube
# todo: rectangles should be drawn only if they are faced to screen else not 
def drawCube(c:Cube):
    cubeCenter = c.getCenter()
    for side in c.getAllSides():
        if hasattr(side, "color") and side.calcAngles(*cubeCenter):
            drawRect(side)

def drawRC(c = rub.cubes):
    for i in range(3):
        for j in range(3):
            for k in range(3):
                t.penup()
                setPoints(c[i][j][k], (3-j)*(clen+2), (3-i)*(clen+2), (3-k)*(clen+2))
                drawCube(c[i][j][k])
    turtle.update()


def refresh():
    t.clear()
    drawRC(rub.cubes)
    sleep(0.2)

drawRC(rub.cubes)

def clicked(point1, point2):
    global xAxis
    global zAxis
    for i in range(18):
        xAxis = (xAxis + 10) % 360
        zAxis = (zAxis + 10) % 360
        refresh()

turtle.update()
s.onclick(clicked)
s._root.mainloop()
