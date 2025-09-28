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
