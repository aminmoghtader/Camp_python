import re
import sys

# ----------------- Product -----------------
class Product:
    used_ids = set()

    def __init__(self, pid, name, price, rating):
        if pid in Product.used_ids:
            raise ValueError("Invalid input")  # آیدی تکراری
        self._id = pid
        self._name = name
        self._price = price
        self._rating = rating
        # کارخانه سازنده
        if 1 <= pid <= 5:
            self._factory = "a"
        elif 5 < pid <= 10:
            self._factory = "b"
        else:
            self._factory = "c"
        Product.used_ids.add(pid)

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


# ----------------- Category -----------------
class Category:
    valid_categories = {
        "Phone": 1, "Car": 2, "Watch": 3, "T-shirt": 4,
        "Laptop": 5, "Tablet": 6, "Charger": 7,
        "Glass": 8, "Robot": 9
    }

    def __init__(self, name):
        if name not in Category.valid_categories:
            raise ValueError("Invalid input")
        self._id = Category.valid_categories[name]
        self._name = name
        self.products = []

    def add_products(self, products):
        self.products.extend(products)

    def filter_by_price(self, low, high):
        result = [p for p in self.products if low <= p.price <= high]
        return result

    def show_supply(self):
        return sorted(self.products, key=lambda p: p.price)

    @property
    def id(self): return self._id
    @property
    def name(self): return self._name


# ----------------- People -----------------
class People:
    def __init__(self, name, surname, age, phone):
        self.name = name
        self.surname = surname
        self.age = age
        if not re.fullmatch(r"09\d{9}", phone):
            raise ValueError("Invalid input")
        self.phone = phone


# ----------------- Cart -----------------
class Cart:
    def __init__(self, owner):
        self.owner = owner
        self.products = []

    def add_products(self, products):
        self.products.extend(products)

    def calculate_price(self):
        total = 0
        print(f"Owner: {self.owner.name} {self.owner.surname}, Phone: {self.owner.phone}")
        for p in self.products:
            print(f"Product: {p.name}, Price: {p.price:.2f}")
            total += p.price
        print(f"Total Price: {total:.2f}")


# ----------------- Main Program -----------------
def main():
    categories = {}
    cart = None

    while True:
        try:
            print("Please choose")
            print("Cart for managing cart")
            print("Category for managing categories")
            print("Exit for exiting the program")
            choice = input().strip()

            if choice == "Exit":
                sys.exit()

            elif choice == "Category":
                cname = input("Enter category name (Phone, Car, Watch, T-shirt, Laptop, Tablet,\nCharger, Glass, Robot):\n").strip()
                try:
                    if cname not in categories:
                        categories[cname] = Category(cname)
                    category = categories[cname]
                except:
                    print("Invalid input")
                    continue

                while True:
                    print("Please choose")
                    print("AddProductCategory for adding products to category")
                    print("FilterByPrice for filtering products by price")
                    print("ShowSupply for showing sorted products")
                    print("Back for returning to main menu")
                    sub_choice = input().strip()

                    if sub_choice == "Back":
                        break
                    elif sub_choice == "AddProductCategory":
                        try:
                            n = int(input("Enter number of products to add:\n"))
                            if n <= 0:
                                raise ValueError
                            new_products = []
                            for _ in range(n):
                                pid = int(input("Enter product ID:\n"))
                                name = input("Enter product name:\n").strip()
                                price = float(input("Enter product price:\n"))
                                rating = float(input("Enter product rating (0-5):\n"))
                                # validate rating range and non-negative price
                                if price < 0 or not (0 <= rating <= 5):
                                    raise ValueError
                                new_products.append(Product(pid, name, price, rating))
                            category.add_products(new_products)
                            print("Products added successfully")
                        except:
                            print("Invalid input")
                    elif sub_choice == "FilterByPrice":
                        try:
                            parts = input().split()
                            if len(parts) != 2:
                                raise ValueError
                            low, high = map(float, parts)
                            if low < 0 or high < 0 or low > high:
                                raise ValueError
                            result = category.filter_by_price(low, high)
                            print(f"Category: {category.name}, ID: {category.id}")
                            if result:
                                for p in result:
                                    print(f"Product: {p.name}, Price: {p.price:.2f}")
                            else:
                                print("No products found")
                        except:
                            print("Invalid input")
                    elif sub_choice == "ShowSupply":
                        try:
                            result = category.show_supply()
                            print(f"Category: {category.name}, ID: {category.id}")
                            if result:
                                for p in result:
                                    print(f"Product: {p.name}, Price: {p.price:.2f}")
                            else:
                                print("No products found")
                        except:
                            print("Invalid input")
                    else:
                        print("Invalid input")

            elif choice == "Cart":
                try:
                    name = input("Enter name:\n").strip()
                    surname = input("Enter surname:\n").strip()
                    age = int(input("Enter age:\n"))
                    # age validation
                    if not (0 <= age <= 120):
                        raise ValueError
                    phone = input("Enter phone:\n").strip()
                    person = People(name, surname, age, phone)
                    cart = Cart(person)
                except:
                    print("Invalid input")
                    continue

                while True:
                    print("Please choose")
                    print("AddProductToCart for adding products to cart")
                    print("CalculatePrice for calculating total price")
                    print("Back for returning to main menu")
                    sub_choice = input().strip()

                    if sub_choice == "Back":
                        break
                    elif sub_choice == "AddProductToCart":
                        try:
                            n = int(input("Enter number of products:\n"))
                            if n <= 0:
                                raise ValueError
                            new_products = []
                            for _ in range(n):
                                pid = int(input("Enter product ID:\n"))
                                name_p = input("Enter product name:\n").strip()
                                price = float(input("Enter product price:\n"))
                                rating = float(input("Enter product rating (0-5):\n"))
                                if price < 0 or not (0 <= rating <= 5):
                                    raise ValueError
                                new_products.append(Product(pid, name_p, price, rating))
                            cart.add_products(new_products)
                            print("Products added to cart successfully")
                        except:
                            print("Invalid input")
                    elif sub_choice == "CalculatePrice":
                        try:
                            if cart is None:
                                print("Invalid input")
                            else:
                                if not cart.products:
                                    # still print owner info and total 0
                                    print(f"Owner: {cart.owner.name} {cart.owner.surname}, Phone: {cart.owner.phone}")
                                    print("Total Price: 0.00")
                                else:
                                    cart.calculate_price()
                        except:
                            print("Invalid input")
                    else:
                        print("Invalid input")

            else:
                print("Invalid input")

        except SystemExit:
            # exit gracefully
            return
        except:
            print("Invalid input")


if __name__ == "__main__":
    main()
