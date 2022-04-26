# import random

class C:
    def __init__(self, cval):
        self.cval = cval

class B:
    def __init__(self, sc):
        self.sc = sc

class A:
    def __init__(self, a):
        self.a = C(a)
        self.b = B(self.a)
    
    # def __lt__(self, other):
    #     print(self.a, other.a)
    #     return self.a < other.a

# arr = [A(random.randint(0, 20)) for i in range(40)]

# for el in arr:
#     print( el.a )

# arr.sort()

# for el in arr:
#     print( el.__getattribute__("a") )

jas = A(45)
jas.b.sc.cval = 46
print(jas.a.cval)
