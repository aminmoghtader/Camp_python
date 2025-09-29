import re
import sys

class Product:
    ids = set()

    def __init__(self, pid, name, price, rating):
        if pid in Product.ids:
            raise ValueError("In valid")
        self._id = pid
        self._name = name
        self._price = price
        self._rating = rating

        if 1 <= pid <= 5:
            self._factory = "a"
        elif 5 <= pid <= 10:
            self._factory = "b"
        else:
            self._factory = "c"
        
        Product.ids.add(pid)

    @property
    def id(self): return self._id
    @property
    def name(self): return self._name
    @property
    def price(self): return self._price
    @property
    def rating(self): return self._rating
    @property
    def factory(self): return self._factory

class Category:

    valid_categories = {
        "Phone": 1, "Car": 2, "Watch": 3, "T-shirt": 4,
        "Laptop": 5, "Tablet": 6, "Charger": 7,
        "Glass": 8, "Robot": 9
    }         

    def __init__(self, name):

        if name not in Category.valid_categories:
            raise ValueError("Invalid")
        self._name = name
        self._id = Category.valid_categories[name]
        self.products = []

    def add(self,products):
        self.products.extend(products)

    def filter(self, low, high):
        result = []
        for p in self.products:
            if  low <= p.price <= high:
                result.append(p) 
        return result

    def supply(self):
        return sorted(self.products, key=lambda p: p.price)
    
    @property
    def id(self): return self._id
    @property
    def name(self): return self._name

class People:

    def __init__(self, name, surname, age, phone):
        self.name = name
        self.surname = surname
        self.age = age     
        if not re.fullmatch(r"09\d{9}", phone):
            raise ValueError("Invalid")
        self.phone = phone

class Cart:
    def __init__(self, owner):
        self.owner = owner
        self.products = []

    def AddProductToCart(self, products):
        self.products.extend(products)
    
    def CalculatePrice(self):
        total = 0
        print(f"Owner: {self.owner.name} {self.owner.surname}, Phone: {self.owner.phone}")
        for p in self.products:
            print(f"product: {p.name}, price: {p.price:.2f}")
            total += p.price
        print(f"total: {total:.2f}")


def main():
    categories = {}
    cart = None

    while True:
        try:
            print("Please choose")
            print("Cart for managing cart")
            print("Category for managing categories")
            print("Exit for exiting the program")
            choose = input().strip()

            if choose == "exit":
                sys.exit()
            elif choose == "category":
                cname = input("Enter category name (Phone, Car, Watch, T-shirt, Laptop, Tablet,\nCharger, Glass, Robot):\n").strip()
                if categories[cname] in Category(cname):
                    category = categories[cname]
                else:
                    continue

                while True:
                    print("Please choose")
                    print("AddProductCategory for adding products to category")
                    print("FilterByPrice for filtering products by price")
                    print("ShowSupply for showing sorted products")
                    print("Back for returning to main menu")
                    sub_choice = input().strip()  

                    if sub_choice == "back":
                        break
                    elif sub_choice == "AddProductCategory":
                        try:
                            n = int(input("Enter number of products to add:\n"))
                            if n <= 0:
                                raise ValueError
                            new = []
                            for _ in range(n):
                                pid = int(input("Enter product ID:\n"))
                                name = input("Enter product name:\n").strip()
                                price = float(input("Enter product price:\n"))
                                rating = float(input("Enter product rating (0-5):\n"))   
                                if price < 0 or not (0 <= rating <= 5):
                                    raise ValueError
                                new.append(Product(pid,name,price,rating))
                            category.AddProductToCart(new)
                            print("ok")
                        except:
                            print("invalid")
                    
                    elif sub_choice == "FilterByPrice":
                        try:
                            part = input().split()
                            if len(part) != 2:
                                raise ValueError
                            low,high = map(float, part)
                            if low > high or low < 0 or high < 0:
                                raise ValueError
                            res = category.filter(low,high)
                            print(f"Category: {category.name}, ID: {category.id}")
                            if res:
                                for p in res:
                                    print(f"Product: {p.name}, Price: {p.price:.2f}")
                            else:
                                print("no")
                        except:
                            print("invalid")
                            


                            
                
