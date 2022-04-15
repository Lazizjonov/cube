# This code is written by Lazizjonov Jasurbek
# 12.04.2022 Tashkent, Uzbekistan.

# Implementation of Rubick's Cube (RC) with python turtle
# To date I developed view of RC and made some refresh function to clean screen and redraw RC (with different angles) from different views




from time import sleep
import turtle
import math
from unicodedata import name

rad = math.radians

# redefining sinus and cosinus functions to use in light form
def sin(x):
    return math.sin(rad(x))

def cos(x):
    return math.cos(rad(x))

pi = math.pi
# colors = ["white", "red", "blue", "orange", "green", "yellow"]
xAxis = 315
yAxis = 90
zAxis = 225
clen = 40

class Point:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def changePoint(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # takePoint2D() function takes 3d point and returns its 2d transition given degrees of all 3 axes
    def takePoint2D(self, xa = xAxis, ya = yAxis, za = zAxis):
        y = self.y * sin(ya) + self.x * sin(xa) + self.z * sin(za)
        x = self.y * cos(ya) + self.x * cos(xa) + self.z * cos(za)
        return (x, y)

    # rotatePoint2D() function takes:
    #     "xc", "yc" coordinates of the center of rotation
    #     rotation angle "alfa" of the given point 
    # returns new "x" and "y" coordinates
    def rotatePoint2D(self, xc, yc, alfa):
        self.x = (  (self.x - xc) * cos(alfa) - (self.y - yc) * sin(alfa)  ) + xc
        self.y = (  (self.y - xc) * sin(alfa) + (self.y - yc) * cos(alfa)  ) + yc



class Rect():
    def __init__(self, color, next = None):
        self.p1 = Point(0,0,0)
        self.p2 = Point(0,0,0)
        self.p3 = Point(0,0,0)
        self.p4 = Point(0,0,0)
        self.color = color
        self.next = next
    
    def getCenter(self):
        return [ (self.p1.x + self.p3.x)/2, (self.p1.y + self.p3.y)/2, (self.p1.z + self.p3.z)/2 ]

    # calcAngles() implements calculation on vector from the center of cube (cx, cy, cz) to center of rect (myCenter) 
    # and returns vector to calculate if it is visible or not
    def calcAngles(self, cx, cy, cz):
        myCenter = self.getCenter()
        print(myCenter[0], cx, myCenter[1], cy, myCenter[2], cz)
        return myCenter[0] + cx >= 0 and myCenter[1] + cy >= 0 and myCenter[2] + cz >= 0

    # Function to draw rectangle side of a single cube
    def drawRect(self, t:turtle.Turtle):
        t.fillcolor(self.color)
        t.penup()
        t.setpos(self.p1.takePoint2D())
        t.begin_fill()
        t.setpos(self.p2.takePoint2D())
        t.setpos(self.p3.takePoint2D())
        t.setpos(self.p4.takePoint2D())
        t.setpos(self.p1.takePoint2D())
        t.end_fill()


# Each cube has 6 sides some sides has attribute color others are linked to other 
# cube that is positioned exactly at that side. 
# This link is supposed to help during rotation of cube parts



class Cube():
    def __init__(self, t, xPos=0, yPos=0, zPos=0):
        self.xSide = Rect("no")
        self.ySide = Rect("no")
        self.zSide = Rect("no")
        self.mxSide = Rect("no")
        self.mySide = Rect("no")
        self.mzSide = Rect("no")
        self.xPos = xPos
        self.yPos = yPos
        self.zPos = zPos
        self.t = t

    def getAllSides(self):
        return (self.xSide, self.ySide, self.zSide, self.mxSide, self.mySide, self.mzSide) 

    def getCenter(self):
        return (self.xPos - clen/2, self.yPos - clen/2, self.zPos - clen/2)

    # Function to draw a single cube
    # It calls drawRect function 6 times to draw all six sides (rectangles) of cube
    # todo: rectangles should be drawn only if they are faced to screen else not 
    def drawCube(self, t):
        cubeCenter = self.getCenter()
        for side in self.getAllSides():
            if side.color != "no" and side.calcAngles(*cubeCenter):
                side.drawRect(t)
    
    # setPoints() function sets points of a single cube which is passed as first argument in the position xp, yp, zp
    # 3 default arguments are x,y,z axis on 3d implemented in 2d
    def setPoints(self, xp, yp, zp):
        if (self.xSide.color != "no"):
            self.xSide.p1.changePoint(xp, yp, zp)
            self.xSide.p2.changePoint(xp, yp - clen, zp)
            self.xSide.p3.changePoint(xp, yp - clen, zp - clen)
            self.xSide.p4.changePoint(xp, yp, zp - clen)
        if (self.ySide.color != "no"):
            self.ySide.p1.changePoint(xp, yp, zp)
            self.ySide.p2.changePoint(xp, yp, zp - clen)
            self.ySide.p3.changePoint(xp - clen, yp, zp - clen)
            self.ySide.p4.changePoint(xp - clen, yp, zp)
        if (self.zSide.color != "no"):
            self.zSide.p1.changePoint(xp, yp, zp)
            self.zSide.p2.changePoint(xp - clen, yp, zp)
            self.zSide.p3.changePoint(xp - clen, yp - clen, zp)
            self.zSide.p4.changePoint(xp, yp - clen, zp)
        if (self.mxSide.color != "no"):
            self.mxSide.p1.changePoint(xp - clen, yp, zp)
            self.mxSide.p2.changePoint(xp - clen, yp, zp - clen)
            self.mxSide.p3.changePoint(xp - clen, yp - clen, zp - clen)
            self.mxSide.p4.changePoint(xp - clen, yp - clen, zp)
        if (self.mySide.color != "no"):
            self.mySide.p1.changePoint(xp, yp - clen, zp)
            self.mySide.p2.changePoint(xp - clen, yp - clen, zp)
            self.mySide.p3.changePoint(xp - clen, yp - clen, zp - clen)
            self.mySide.p4.changePoint(xp, yp - clen, zp - clen)
        if (self.mzSide.color != "no"):
            self.mzSide.p1.changePoint(xp, yp, zp - clen)
            self.mzSide.p2.changePoint(xp, yp - clen, zp - clen)
            self.mzSide.p3.changePoint(xp - clen, yp - clen, zp - clen)
            self.mzSide.p4.changePoint(xp - clen, yp, zp - clen)


# Rubick's cube contains 27 single cubes united in traditional form 3x3x3
# rubics object contains cubes matrix which is 3x3x3 size
class rubics:
    def __init__(self, t):
        self.t = t
        self.cubes = [[[[], [], []], [[], [], []], [[], [], []]], [[[], [], []], [[], [], []], [[], [], []]], [[[], [], []], [[], [], []], [[], [], []]]]
        for i in range(3):
            # self.cubes.append([])
            for j in range(3):
                # self.cubes[i].append([])
                for k in range(3):
                    # self.cubes[i][j].append([])
                    self.cubes[i][j][k] = Cube(t)

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if i==0:
                        self.cubes[i][j][k].ySide.color="white"
                    if j==0:
                        self.cubes[i][j][k].xSide.color="blue"
                    if k==0:
                        self.cubes[i][j][k].zSide.color="red"
                    if j==2:
                        self.cubes[i][j][k].mxSide.color="green"
                    if k==2:
                        self.cubes[i][j][k].mzSide.color="orange"
                    if i==2:
                        self.cubes[i][j][k].mySide.color="yellow"
                    if i==1:
                        self.cubes[i-1][j][k].mySide.next = self.cubes[i][j][k]
                        self.cubes[i][j][k].ySide.next = self.cubes[i-1][j][k]
                        self.cubes[i][j][k].mySide.next = self.cubes[i+1][j][k]
                        self.cubes[i+1][j][k].ySide.next = self.cubes[i][j][k]
                    if j==1:
                        self.cubes[i][j-1][k].mxSide.next = self.cubes[i][j][k]
                        self.cubes[i][j][k].xSide.next = self.cubes[i][j-1][k]
                        self.cubes[i][j+1][k].xSide.next = self.cubes[i][j][k]
                        self.cubes[i][j][k].mxSide.next = self.cubes[i][j+1][k]
                    if k==1:
                        self.cubes[i][j][k-1].mzSide.next = self.cubes[i][j][k]
                        self.cubes[i][j][k].zSide.next = self.cubes[i][j][k-1]
                        self.cubes[i][j][k+1].zSide.next = self.cubes[i][j][k]
                        self.cubes[i][j][k].mzSide.next = self.cubes[i][j][k+1]

    def drawRC(self, t):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.cubes[i][j][k].setPoints( (3-j)*(clen+2), (3-i)*(clen+2), (3-k)*(clen+2) )
                    self.cubes[i][j][k].drawCube(t)

    def clicked(self, point1, point2):
        for i in range(18):

            self.refresh()
    
    # turtle.tracer(0, 0) is used to make the speed of turtle object as fast as possible
    # it is used with turtle.update() function at the end of movement to display changes.
    

    
    
    def refresh(self):
        self.t.clear()
        self.drawRC(self.t)
        turtle.update()
        sleep(0.2)


if( __name__ == "__main__" ):
    turtle.tracer(0, 0)
    t = turtle.getturtle()
    t.hideturtle()
    t.speed(0)
    s = t.getscreen()
    s.bgcolor("silver")
    t.penup()
    t.pencolor('black')
    turtle.update()
    
    rub = rubics(t)

    
    s.onclick(rub.clicked)
    s._root.mainloop()

# todo: rotation of whole RC