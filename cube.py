from time import sleep
import turtle
import math

rad = math.radians

def sin(x):
    return math.sin(rad(x))

def cos(x):
    return math.cos(rad(x))

pi = math.pi
colors = ["cyan", "red", "blue", "orange", "green", "yellow"]

num = 0

# turtle.tracer(0, 0)
t = turtle.getturtle()
t.hideturtle()
t.speed(0)
xAxis = 330
yAxis = 90
zAxis = 210
clen = 30

class Cube:
    def __init__(self, xSide=0, ySide=0, zSide=0, mxSide=0, mySide=0, mzSide=0):
        self.xSide, self.ySide, self.zSide, self.mxSide, self.mySide, self.mzSide = ySide, zSide, mxSide, mySide, mzSide, xSide
        self.sides = [xSide, ySide, zSide, mxSide, mySide, mzSide]
    


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
                    cubes[i][j][k].ySide = "cyan"
                if j==0:
                    cubes[i][j][k].xSide = "blue"
                if k==0:
                    cubes[i][j][k].zSide = "red"
                if j==2:
                    cubes[i][j][k].mxSide = "green"
                if k==2:
                    cubes[i][j][k].mzSide = "orange"
                if i==2:
                    cubes[i][j][k].mySide = "yellow"
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

def drawRect(inaxe):
    if inaxe in ["mx", "my", "mz"]:
        t.setheading(yAxis+180)
        t.forward(clen)
        t.setheading(xAxis+180)
        t.forward(clen)
        t.setheading(zAxis+180)
        t.forward(clen)
    t.begin_fill()
    if inaxe == "x":
        t.setheading(yAxis + 180)
        t.forward(clen)
        t.setheading(zAxis + 180)
        t.forward(clen)
        t.setheading(yAxis)
        t.forward(clen)
        t.setheading(zAxis)
        t.forward(clen)
    elif inaxe == "y":
        t.setheading(xAxis + 180)
        t.forward(clen)
        t.setheading(zAxis + 180)
        t.forward(clen)
        t.setheading(xAxis)
        t.forward(clen)
        t.setheading(zAxis)
        t.forward(clen)
    elif inaxe == "z":
        t.setheading(xAxis + 180)
        t.forward(clen)
        t.setheading(yAxis + 180)
        t.forward(clen)
        t.setheading(xAxis)
        t.forward(clen)
        t.setheading(yAxis)
        t.forward(clen)
    elif inaxe == "mx":
        t.setheading(yAxis)
        t.forward(clen)
        t.setheading(zAxis)
        t.forward(clen)
        t.setheading(yAxis + 180)
        t.forward(clen)
        t.setheading(zAxis + 180)
        t.forward(clen)
    elif inaxe == "my":
        t.setheading(xAxis)
        t.forward(clen)
        t.setheading(zAxis)
        t.forward(clen)
        t.setheading(xAxis + 180)
        t.forward(clen)
        t.setheading(zAxis + 180)
        t.forward(clen)
    elif inaxe == "mz":
        t.setheading(xAxis)
        t.forward(clen)
        t.setheading(yAxis)
        t.forward(clen)
        t.setheading(xAxis + 180)
        t.forward(clen)
        t.setheading(yAxis + 180)
        t.forward(clen)
    t.end_fill()

def drawCube(c, xpos, ypos, zpos):
    y = ypos*sin(yAxis) + xpos*sin(xAxis) + zpos*sin(zAxis)
    x = ypos*cos(yAxis) + xpos*cos(xAxis) + zpos*cos(zAxis)
    t.penup()
    t.setpos(x,y)
    t.pendown()
    if c.xSide in colors:
        t.color(c.xSide)
        drawRect("x")
    if c.ySide in colors:
        t.color(c.ySide)
        drawRect("y")
    if c.zSide in colors:
        t.color(c.zSide)
        drawRect("z")
    if c.mxSide in colors:
        t.color(c.mxSide)
        drawRect("mx")
    if c.mySide in colors:
        t.color(c.mySide)
        drawRect("my")
    if c.mzSide in colors:
        t.color(c.mzSide)
        drawRect("mz")


def clicked(point1, point2):
    print(point1, point2)

s = t.getscreen()

for i in range(3):
    drawCube(rub.cubes[i][0][0], (2-i)*40, (0)*40, (0)*40)


def drawPoint(xpos, ypos, zpos):
    y = ypos*sin(yAxis) + xpos*sin(xAxis) + zpos*sin(zAxis)
    x = ypos*cos(yAxis) + xpos*cos(xAxis) + zpos*cos(zAxis)
    t.setpos(x,y)

# turtle.update()
# sleep(3)


# s.onclick(clicked)
# s._root.mainloop()
