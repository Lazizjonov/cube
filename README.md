# cube.py
rubick's cube on python turtle :)

> Python's turtle graphic is too simple and I wanted to reach its limits by implementing 3d game with that

This code is simply used to draw red rectangle
```python
  import turtle
  t = turtle.getturtle()
  t.fillcolor('red')
  t.begin_fill()
  t.setpos(0, 50)
  t.setpos(50, 50)
  t.setpos(50, 0)
  t.setpos(0, 0)
  t.end_fill()
```
and I just made it a little bit complex with transition of point from 3D to 2D by the function takePoint2D()

```python
  import math
  
  def sin(x:float):
    return math.sin(math.radians(x))
    
  def cos(x:float):
    return math.cos(math.radians(x))
    
  def takePoint2D(x, y, z, xa = 315, ya = 90, za = 225):
    y2D = y * sin(ya) + x * sin(xa) + z * sin(za)
    x2D = y * cos(ya) + x * cos(xa) + z * cos(za)
    return (x2D, y2D)
```

For rotation animations I used 3D rotation matrix which is implemented as a function rotatePoint3D()
Rotation of a given point coordinates x, y, z is made relative to line formed by point v1 and point v2 (they have components x, y, z)
```python
  def vectorMagnitude(x, y, z):
    return( math.sqrt( x**2 + y**2 + z**2 ) )
    
  def vectorToUnit(x, y, z):
    vm = vectorMagnitude(x, y, z)
    return (x/vm, y/vm, z/vm)
    
  def rotatePoint3D(x, y, z, v1, v2, angle):
    ca = cos(angle)
    sa = sin(angle)
    uvx, uvy, uvz = vectorToUnit(v2.x - v1.x, v2.y - v1.y, v2.z - v1.z)
    nx = (x - v1.x) * ( ca + uvx**2 * (1-ca) ) + (y - v1.y) * (uvy * uvx * (1-ca) + uvz * sa) + (z - v1.z) * ( uvz * uvx * (1-ca) - uvy * sa )
    ny = (x - v1.x) * ( uvy * uvx * (1-ca) - uvz * sa) + (y - v1.y) * (ca + uvy**2 * (1-ca) ) + (z - v1.z) * ( uvz * uvy * (1-ca) + uvx * sa )
    nz = (x - v1.x) * ( uvz * uvx * (1-ca) + uvy * sa) + (y - v1.y) * (uvz * uvy * (1-ca) - uvx * sa ) + (z - v1.z) * ( ca + uvz**2 * (1-ca) )
    return nx + v1.x, ny + v1.y, nz + v1.z
```
