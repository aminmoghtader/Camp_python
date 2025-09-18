import math

def Area(r):
	
    if r <= 0:
        return "Out of range"
    else:
        A = math.pi * r ** 2
        if A < 10:
            size = "Small Circle"
        else:
            size = "Big Circle"
        return f"Area = {A:.4f}m^2\n{size}"
        
def perimeter(r):
	
    if r <= 0:
        return "Out of range"
    else:
        p = 2 * math.pi * r
        return f"Perimeter = {p:.4f}m"
		
	
	
r = float(input("please inter your number: "))
print(Area(r))
print(perimeter(r))
