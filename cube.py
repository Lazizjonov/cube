# This code is written by Lazizjonov Jasurbek
# 12.04.2022 Tashkent, Uzbekistan.

# Implementation of Rubick's Cube (RC) with python turtle
# To date Rubick's Cube is fully rotatable by mouse drag
# 26.04.2022 I could rotate one side of RC and currently I am working on a simple algorithm for mouse event connection with rotation functions.




from time import sleep
import turtle
import math
 

pi = math.pi
# colors = ["white", "red", "blue", "orange", "green", "yellow"]
xAxis = 315
yAxis = 90
zAxis = 225
clen = 70
jasVal = math.sqrt(3) * clen / 2


# redefining sinus and cosinus functions to use in light form
def sin(x:float):
    return math.sin(math.radians(x))

def cos(x:float):
    return math.cos(math.radians(x))

def acos(x:float):
    return math.acos(x) * 180 / math.pi

def atan(x:float):
    return math.atan(x) * 180 / pi

# returns vector length from x = 500, y = 500, z = 500 point to p1
def vectorLen(p1):
    # return math.sqrt((p1[0] - 500) ** 2 + (p1[1] - 500) ** 2 + (p1[2] - 500) ** 2)
    return p1[0] + p1[1] + p1[2]

def vectorMagnitude(x, y, z):
    return( math.sqrt( x**2 + y**2 + z**2 ) )

def vectorToUnit(x, y, z):
    vm = vectorMagnitude(x, y, z)
    return (x/vm, y/vm, z/vm)

# function returns 2D line equation (k and c from y = k * x + c) from coordinates of 2 points in 2D
def lineEquation(x1, y1, x2, y2):
    if(x2 - x1 == 0):
        return 1, -x1, 0
    elif(y2 - y1 == 0):
        return 0, y1, 1
    return (y2 - y1) / (x2 - x1), y1 - (x1 * (y2 - y1) / (x2 - x1)), 1

def angleBRC(x1, y1, z1, x2, y2, z2):
    return acos( (x1 - x2 + y1 - y2 + z1 - z2) / jasVal )  


turtle.tracer(0, 0)
t = turtle.getturtle()

class Render:
    def __init__(self, rub):
        self.rub = rub
        self.listOfRects = []
    
    def renderAll(self):
        self.listOfRects.sort()
        for rect in self.listOfRects:
            rect.drawRect()
            # sleep(0.2)
            # turtle.update()

        self.rub.visibleRects = self.listOfRects[27:]
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
        self.y2D = self.y * sin(ya) + self.x * sin(xa) + self.z * sin(za)
        self.x2D = self.y * cos(ya) + self.x * cos(xa) + self.z * cos(za)
        return (self.x2D, self.y2D)

    # rotatePoint2D() function takes:
    #     "xc", "zc" coordinates of the center of rotation
    #     rotation angle "alfa" of the given point 
    # returns new "x" and "z" coordinates
    def rotatePoint2D(self, cx, cz, alfa:float, betta:float = 0, gamma:float = 0):
        self.x, self.z = self.frotatePoint2D(self.x, self.z, cx, cz, alfa)
        self.y, self.z = self.frotatePoint2D(self.y, self.z, cx, cz, betta)
        self.y, self.x = self.frotatePoint2D(self.y, self.x, cx, cz, gamma)

    def frotatePoint2D(self, px, py, cx, cy, alfa:float):
        cosine = math.cos(math.radians(alfa))
        sine = math.sin(math.radians(alfa))
        x = (px - cx)  * cosine - (py - cy) * sine
        y = (px - cx) * sine + (py - cy) * cosine
        return x + cx, y + cy

    def rotatePoint3D(self, v1, v2, angle):
        ca = cos(angle)
        sa = sin(angle)
        uvx, uvy, uvz = vectorToUnit(v2.x - v1.x, v2.y - v1.y, v2.z - v1.z)
        x = (self.x - v1.x) * ( ca + uvx**2 * (1-ca) ) + (self.y - v1.y) * (uvy * uvx * (1-ca) + uvz * sa) + (self.z - v1.z) * ( uvz * uvx * (1-ca) - uvy * sa )
        y = (self.x - v1.x) * ( uvy * uvx * (1-ca) - uvz * sa) + (self.y - v1.y) * (ca + uvy**2 * (1-ca) ) + (self.z - v1.z) * ( uvz * uvy * (1-ca) + uvx * sa )
        z = (self.x - v1.x) * ( uvz * uvx * (1-ca) + uvy * sa) + (self.y - v1.y) * (uvz * uvy * (1-ca) - uvx * sa ) + (self.z - v1.z) * ( ca + uvz**2 * (1-ca) )
        self.x, self.y, self.z = x + v1.x, y + v1.y, z + v1.z



class Rect():
    def __init__(self, color, sc:Point, cube):
        self.p1 = Point(0,0,0)
        self.p2 = Point(0,0,0)
        self.p3 = Point(0,0,0)
        self.p4 = Point(0,0,0)
        self.color = color
        self.dependCube = cube
        self.sc = sc
    
    # function to get center of Rectangle by calculating arithmetic avarage of current positions of 1st and 3rd points
    def getCenter(self):
        return [ (self.p1.x + self.p3.x)/2, (self.p1.y + self.p3.y)/2, (self.p1.z + self.p3.z)/2 ]

    def isinside(self, ex, ey):
        k1, c1, j1 = lineEquation(*self.pd1, *self.pd2)
        k2, c2, j2 = lineEquation(*self.pd2, *self.pd3)
        k3, c3, j3 = lineEquation(*self.pd3, *self.pd4)
        k4, c4, j4 = lineEquation(*self.pd4, *self.pd1)
        # return j1 * ey < k1 * ex + c1 and j2 * ey < k2 * ex + c2 and j3 * ey > k3 * ex + c3 and j4 * ey > k4 * ex + c4
        return (
            j1 * ey < k1 * ex + c1 and 
            j2 * ey < k2 * ex + c2 and 
            j3 * ey > k3 * ex + c3 and 
            j4 * ey > k4 * ex + c4
            ) or (
            j1 * ey < k1 * ex + c1 and 
            j2 * ey > k2 * ex + c2 and 
            j3 * ey > k3 * ex + c3 and 
            j4 * ey < k4 * ex + c4
            ) or (
            j1 * ey > k1 * ex + c1 and 
            j2 * ey > k2 * ex + c2 and 
            j3 * ey < k3 * ex + c3 and 
            j4 * ey < k4 * ex + c4
            ) or (
            j1 * ey > k1 * ex + c1 and 
            j2 * ey < k2 * ex + c2 and 
            j3 * ey < k3 * ex + c3 and 
            j4 * ey > k4 * ex + c4
            )

    # __lt__ function allows to sort Rect objects in array which I used in Render object
    def __lt__(self, other):
        # return vectorLen(self.getCenter()) < vectorLen(other.getCenter())
        selfAngle = angleBRC(*self.getCenter(), self.sc.x, self.sc.y, self.sc.z)
        otherAngle = angleBRC(*other.getCenter(), other.sc.x, other.sc.y, other.sc.z)
        if(int(selfAngle*100) == int(otherAngle*100)):
            return vectorLen(self.getCenter()) < vectorLen(other.getCenter())
        return  selfAngle > otherAngle

    # Function to draw rectangle side of a single cube
    def drawRect(self, col = None):
        if(col == None):
            col = self.color
        self.pd1 = self.p1.takePoint2D()
        self.pd2 = self.p2.takePoint2D()
        self.pd3 = self.p3.takePoint2D()
        self.pd4 = self.p4.takePoint2D()
        t.fillcolor(col)
        t.penup()
        t.setpos(self.pd1)
        t.pendown()
        t.begin_fill()
        t.setpos(self.pd2)
        t.setpos(self.pd3)
        t.setpos(self.pd4)
        t.setpos(self.pd1)
        t.end_fill()

    def renderRect(self, ren:Render):
        ren.addRect(self)

    def rotateRect2D(self, xc, yc, alfa, betta, gamma):
        for point in [self.p1, self.p2, self.p3, self.p4]:
            point.rotatePoint2D(xc, yc, alfa, betta, gamma)

    def rotateRect3D(self, v1, v2, angle):
        for point in [self.p1, self.p2, self.p3, self.p4]:
            point.rotatePoint3D(v1, v2, angle)
        


    # def calcAngles(self, cx, cy, cz):
    #     myCenter = self.getCenter()
    #     # xDif, yDif, zDif  = cx - myCenter[0], cy - myCenter[1], cz - myCenter[2]
    #     # if self.color == "red": print("x dif:", "{:.2f}".format(xDif), "\tty dif:", "{:.2f}".format(yDif), "\tz dif:", "{:.2f}".format(zDif))
    #     # return xDif <= clen2 and yDif <= clen2 and zDif <= clen2

    #     # if angle between vector from the center of the cube to the center of the side (Rect) is lower than 90 degrees 
    #     vx, vy, vz = myCenter[0] - cx, myCenter[1] - cy, myCenter[2] - cz
    #     return math.acos((vx + vy + vz) * jasVal) * 180 / pi <= 90


# Each cube has 6 sides some sides has attribute color others are linked to other 
# cube that is positioned exactly at that side. 
# This link is supposed to help during rotation of cube parts



class Cube():
    def __init__(self, xPos, yPos, zPos, i, j, k):
        self.i, self.j, self.k = i, j, k
        self.center = Point(xPos + clen/2, yPos + clen/2, zPos + clen/2)
        self.xSide = Rect("no", self.center, self)
        self.ySide = Rect("no", self.center, self)
        self.zSide = Rect("no", self.center, self)
        self.mxSide = Rect("no", self.center, self)
        self.mySide = Rect("no", self.center, self)
        self.mzSide = Rect("no", self.center, self)
        self.setPoints(xPos, yPos, zPos)

    def getAllSides(self):
        return (self.xSide, self.ySide, self.zSide, self.mxSide, self.mySide, self.mzSide) 

    # Function to draw a single cube
    # It calls renderCube function 6 times to draw all six sides (rectangles) of cube
    def renderCube(self, ren:Render):
        for side in self.getAllSides():
            if side.color != "no":
                side.renderRect(ren)
    
    # setPoints() function sets points of a single cube which is passed as first argument in the position xp, yp, zp
    # 3 default arguments are x,y,z axis on 3d implemented in 2d
    def setPoints(self, xp, yp, zp):
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
    
    def rotateCube2D(self, xc, yc, alfa, betta, gamma):
        self.center.rotatePoint2D(xc, yc, alfa, betta, gamma)
        for rec in self.getAllSides():
            rec.rotateRect2D(xc, yc, alfa, betta, gamma)

    def rotateCube3D(self, cubes, v2, angle):
        v1 = cubes[1][1][1].center
        self.center.rotatePoint3D(v1, v2, angle)
        for rec in self.getAllSides():
            rec.rotateRect3D(v1, v2, angle)

# Rubick's cube contains 27 single cubes united in traditional form 3x3x3
# rubics object contains cubes matrix which is 3x3x3 size
class rubics:
    def __init__(self):
        self.cubes = [[[[], [], []], [[], [], []], [[], [], []]], [[[], [], []], [[], [], []], [[], [], []]], [[[], [], []], [[], [], []], [[], [], []]]]
        self.visibleRects = []
        self.dragFlag = 0
        self.lockRotation = 1
        self.mousePosX = 0
        self.mousePosY = 0
        self.turtlePosX = 0
        self.turtlePosY = 0
        for i in range(3):
            # self.cubes.append([])
            for j in range(3):
                # self.cubes[i].append([])
                for k in range(3):
                    # self.cubes[i][j].append([])
                    self.cubes[i][j][k] = Cube( i * clen, j * clen , k* clen, i, j, k)
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


    def turtleClick(self, p1, p2):
        self.turtlePosX, self.turtlePosY = p1, p2

    def drawRC(self, ren:Render):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.cubes[i][j][k].renderCube(ren)
        ren.renderAll()
    
    # Function to rotate whole RC in 3D
    def rotateRC3D(self, ex, ey):
        xch, ych = ex - self.mousePosX, ey - self.mousePosY
        self.mousePosX, self.mousePosY = ex, ey
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.cubes[i][j][k].rotateCube2D(clen * 3 / 2, clen * 3 / 2, -xch/2, ych/4, ych/4)

    def rotateIJK(self):
        for l in range(15):
            for i in range(3):
                for j in range(3):
                    self.cubes[i][1][j].rotateCube3D(self.cubes, 6)

            
            self.refresh()
            
    def refresh(self):
        t.clear()
        self.drawRC(ren)
        turtle.update()
        # sleep(0.02)
    
    def clicked(self, event):
        self.lockRotation = 0
        self.sideRotationFlag = 0
        self.mousePosX, self.mousePosY = event.x, event.y
        self.xDif, self.yDif = self.turtlePosX - event.x, self.turtlePosY + event.y
        for rect in self.visibleRects:            
            if (rect.isinside(event.x + self.xDif, self.yDif - event.y)):
                self.lockRotation = 1
                self.sideRotationFlag = 1
                self.activeRect = rect
                self.activeRect.drawRect("silver")
                break
                # turtle.update()
                # sleep(0.2)

    def dragging(self, event):
        if( self.dragFlag == 0 and self.lockRotation == 0):
            self.dragFlag = 1
            # print( self.mousePosX, self.mousePosY, event.x, event.y)
            self.rotateRC3D(event.x, event.y)
            self.refresh()
            self.dragFlag = 0

    def onRelease(self, event):
        self.lockRotation = 1
        if(self.sideRotationFlag == 1):
            self.rotateIJK()


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
    ren = Render(rub)
    rub.drawRC(ren)
    s.onclick(rub.turtleClick)

    canvas = turtle.getcanvas()
    root = canvas.winfo_toplevel()
    root.bind('<Motion>', rub.dragging)
    root.bind('<ButtonRelease-1>', rub.onRelease)
    root.bind('<ButtonPress-1>', rub.clicked)
    
    s._root.mainloop()