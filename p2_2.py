import math

class Circle:
    def __init__(self, r, a=0, b=0):
        self.r = r
        self.a = a
        self.b = b

    def perimeter(self):
        return 2 * math.pi * self.r

    def area(self):
        return math.pi * self.r ** 2

    def distance(self, x, y):
        dx = x - self.a
        dy = y - self.b
        return math.sqrt(dx**2 + dy**2)

    def inside(self, x, y):
        d = self.distance(x, y)
        if d < self.r:
            return "in"
        elif d > self.r:
            return "out"
        else:
            return "on"


r, a, b = map(float, input().split())
x, y = map(float, input().split())

c = Circle(r, a, b)

# چاپ خروجی با 2 رقم اعشار
print(f"{c.perimeter():.2f}")
print(f"{c.area():.2f}")
print(f"{c.distance(x, y):.2f}")
print(c.inside(x, y))
