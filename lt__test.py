import random

class A:
    def __init__(self, a):
        self.a = a
    
    def __lt__(self, other):
        print(self.a, other.a)
        return self.a < other.a

arr = [A(random.randint(0, 20)) for i in range(40)]

for el in arr:
    print( el.a )

arr.sort()

for el in arr:
    print( el.__getattribute__("a") )