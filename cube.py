# This code is written by Lazizjonov Jasurbek
# 12.04.2022 Tashkent, Uzbekistan.

# Implementation of Rubick's Cube (RC) with python turtle
# To date I developed view of RC and made some refresh function to clean screen and redraw RC (with different angles) from different views




from time import sleep
import turtle
import math

from matplotlib.pyplot import cla


# redefining sinus and cosinus functions to use in light form
def sin(x:float):
    return math.sin(math.radians(x))

def cos(x:float):
    return math.cos(math.radians(x))

def atan(x:float):
    return math.atan(x) * 180 / pi

def vectorLen(p1):
    return math.sqrt((p1[0] - 500) ** 2 + (p1[1] - 500) ** 2 + (p1[2] - 500) ** 2)

pi = math.pi
# colors = ["white", "red", "blue", "orange", "green", "yellow"]
xAxis = 315
yAxis = 90
zAxis = 225
clen = 70
clen2 = clen / 2 * sin(45)

turtle.tracer(0, 0)
t = turtle.getturtle()

class Render():
    listOfRects = []
    
    def renderAll(self):
        self.listOfRects.sort()
        for rect in self.listOfRects:
            rect.drawRect()
            # sleep(0.2)
            # turtle.update()

        self.listOfRects = []

    def addRect(self, rect):
        self.listOfRects.append(rect)

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
    #     "xc", "zc" coordinates of the center of rotation
    #     rotation angle "alfa" of the given point 
    # returns new "x" and "z" coordinates
    def rotatePoint2D(self, cx, cz, alfa:float):
        self.x, self.z = self.frotatePoint2D(self.x, self.z, cx, cz, alfa)

    def frotatePoint2D(self, px, py, cx, cy, alfa:float):
        cosine = math.cos(math.radians(alfa))
        sine = math.sin(math.radians(alfa))
        x = (px - cx)  * cosine - (py - cy) * sine
        y = (px - cx) * sine + (py - cy) * cosine
        return x + cx, y + cy



class Rect():
    def __init__(self, color):
        self.p1 = Point(0,0,0)
        self.p2 = Point(0,0,0)
        self.p3 = Point(0,0,0)
        self.p4 = Point(0,0,0)
        self.color = color
    
    def getCenter(self):
        return [ (self.p1.x + self.p3.x)/2, (self.p1.y + self.p3.y)/2, (self.p1.z + self.p3.z)/2 ]


    def __lt__(self, other):
        return vectorLen(self.getCenter()) > vectorLen(other.getCenter())

    # Function to draw rectangle side of a single cube
    def drawRect(self):
        t.fillcolor(self.color)
        t.penup()
        t.setpos(self.p1.takePoint2D())
        t.pendown()
        t.begin_fill()
        t.setpos(self.p2.takePoint2D())
        t.setpos(self.p3.takePoint2D())
        t.setpos(self.p4.takePoint2D())
        t.setpos(self.p1.takePoint2D())
        t.end_fill()

    def renderRect(self, ren:Render):
        ren.addRect(self)

    def rotateRect2D(self, xc, yc, alfa):
        for point in [self.p1, self.p2, self.p3, self.p4]:
            point.rotatePoint2D(xc, yc, alfa)

# Each cube has 6 sides some sides has attribute color others are linked to other 
# cube that is positioned exactly at that side. 
# This link is supposed to help during rotation of cube parts



class Cube():
    def __init__(self, xPos=0, yPos=0, zPos=0):
        self.xSide = Rect("no")
        self.ySide = Rect("no")
        self.zSide = Rect("no")
        self.mxSide = Rect("no")
        self.mySide = Rect("no")
        self.mzSide = Rect("no")
        self.center = Point(xPos, yPos, zPos)

    def getAllSides(self):
        return (self.xSide, self.ySide, self.zSide, self.mxSide, self.mySide, self.mzSide) 

    def getCenter(self):
        return ((self.mxSide.p1.x + self.xSide.p1.x) / 2, (self.mxSide.p1.y + self.xSide.p1.y) / 2, (self.mxSide.p1.z + self.xSide.p1.z) / 2)

    # Function to draw a single cube
    # It calls renderCube function 6 times to draw all six sides (rectangles) of cube
    def renderCube(self, ren:Render):
        cubeCenter = self.getCenter()
        for side in self.getAllSides():
            if side.color != "no":
                side.renderRect(ren)
    
    # setPoints() function sets points of a single cube which is passed as first argument in the position xp, yp, zp
    # 3 default arguments are x,y,z axis on 3d implemented in 2d
    def setPoints(self, xp, yp, zp):
        self.center.x = xp
        self.center.y = yp
        self.center.z = zp
        
        self.xSide.p1.changePoint(xp + clen, yp + clen, zp + clen)
        self.xSide.p2.changePoint(xp + clen, yp + clen, zp)
        self.xSide.p3.changePoint(xp + clen, yp, zp)
        self.xSide.p4.changePoint(xp + clen, yp, zp + clen)
    
        self.ySide.p1.changePoint(xp, yp + clen, zp)
        self.ySide.p2.changePoint(xp, yp + clen, zp + clen)
        self.ySide.p3.changePoint(xp + clen, yp + clen, zp + clen)
        self.ySide.p4.changePoint(xp + clen, yp + clen, zp)
    
        self.zSide.p1.changePoint(xp + clen, yp + clen, zp + clen)
        self.zSide.p2.changePoint(xp, yp + clen, zp + clen)
        self.zSide.p3.changePoint(xp, yp, zp + clen)
        self.zSide.p4.changePoint(xp + clen, yp, zp + clen)
    
        self.mxSide.p1.changePoint(xp, yp, zp)
        self.mxSide.p2.changePoint(xp, yp, zp + clen)
        self.mxSide.p3.changePoint(xp, yp + clen, zp + clen)
        self.mxSide.p4.changePoint(xp, yp + clen, zp)
    
        self.mySide.p1.changePoint(xp, yp, zp)
        self.mySide.p2.changePoint(xp + clen, yp, zp)
        self.mySide.p3.changePoint(xp + clen, yp, zp + clen)
        self.mySide.p4.changePoint(xp, yp, zp + clen)
    
        self.mzSide.p1.changePoint(xp, yp, zp)
        self.mzSide.p2.changePoint(xp + clen, yp, zp)
        self.mzSide.p3.changePoint(xp + clen, yp + clen, zp)
        self.mzSide.p4.changePoint(xp, yp + clen, zp)
    
    def rotateCube2D(self, xc, yc, alfa):
        self.center.rotatePoint2D(xc, yc, alfa)
        for rec in self.getAllSides():
            rec.rotateRect2D(xc, yc, alfa)

# Rubick's cube contains 27 single cubes united in traditional form 3x3x3
# rubics object contains cubes matrix which is 3x3x3 size
class rubics:
    def __init__(self):
        self.cubes = [[[[], [], []], [[], [], []], [[], [], []]], [[[], [], []], [[], [], []], [[], [], []]], [[[], [], []], [[], [], []], [[], [], []]]]
        self.dragFlag = 0
        self.lockRotation = 1
        for i in range(3):
            # self.cubes.append([])
            for j in range(3):
                # self.cubes[i].append([])
                for k in range(3):
                    # self.cubes[i][j].append([])
                    self.cubes[i][j][k] = Cube()

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if i==0:
                        self.cubes[i][j][k].mxSide.color="green"
                    if j==0:
                        self.cubes[i][j][k].mySide.color="yellow"
                    if k==0:
                        self.cubes[i][j][k].mzSide.color="orange"
                    if j==2:
                        self.cubes[i][j][k].ySide.color="white"
                    if k==2:
                        self.cubes[i][j][k].zSide.color="red"
                    if i==2:
                        self.cubes[i][j][k].xSide.color="blue"
                    # if i==1:
                    #     self.cubes[i-1][j][k].xSide.next = self.cubes[i][j][k]
                    #     self.cubes[i][j][k].mxSide.next = self.cubes[i-1][j][k]
                    #     self.cubes[i][j][k].xSide.next = self.cubes[i+1][j][k]
                    #     self.cubes[i+1][j][k].mxSide.next = self.cubes[i][j][k]
                    # if j==1:
                    #     self.cubes[i][j-1][k].ySide.next = self.cubes[i][j][k]
                    #     self.cubes[i][j][k].mySide.next = self.cubes[i][j-1][k]
                    #     self.cubes[i][j+1][k].mySide.next = self.cubes[i][j][k]
                    #     self.cubes[i][j][k].ySide.next = self.cubes[i][j+1][k]
                    # if k==1:
                    #     self.cubes[i][j][k-1].zSide.next = self.cubes[i][j][k]
                    #     self.cubes[i][j][k].mzSide.next = self.cubes[i][j][k-1]
                    #     self.cubes[i][j][k+1].mzSide.next = self.cubes[i][j][k]
                    #     self.cubes[i][j][k].zSide.next = self.cubes[i][j][k+1]

    def firsDrawRC(self, ren:Render):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.cubes[i][j][k].setPoints( i*(clen), j*(clen), k*(clen) )
                    self.cubes[i][j][k].renderCube(ren)
        ren.renderAll()
    def drawRC(self):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.cubes[i][j][k].renderCube(ren)
        ren.renderAll()
    
        
    def rotateRC2D(self):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.cubes[i][j][k].rotateCube2D(clen * 3 / 2, clen * 3 / 2, 3)
    
    def rotateIJK(self):
        for i in range(3):
            for k in range(3):
                    self.cubes[i][2][k].rotateCube2D(clen * 3 / 2, clen * 3 / 2, -3)
            
    def refresh(self):
        t.clear()
        self.drawRC()
        turtle.update()
        # sleep(0.02)
    
    def clicked(self, point1, point2):
        self.lockRotation = 0
        for i in range(30):
            # print(i)
            self.rotateIJK()
            self.refresh()

    def dragging(self, event):
        if( self.dragFlag == 0 and self.lockRotation == 0):
            self.dragFlag = 1
            self.rotateRC2D()
            self.refresh()
            self.dragFlag = 0

    def onRelease(self, event):
        self.lockRotation = 1


# turtle.tracer(0, 0) is used to make the speed of turtle object as fast as possible
# it is used with turtle.update() function at the end of movement to display changes.

if( __name__ == "__main__" ):
    t.hideturtle()
    t.speed(0)
    s = t.getscreen()
    s.bgcolor("silver")
    t.color("grey")
    t.pensize(2)    
    turtle.update()
    
    rub = rubics()
    ren = Render()
    rub.firsDrawRC(ren)

    canvas = turtle.getcanvas()
    root = canvas.winfo_toplevel()
    root.bind('<Motion>', rub.dragging)
    root.bind('<ButtonRelease>', rub.onRelease)
    s.onclick(rub.clicked)
    
    s._root.mainloop()