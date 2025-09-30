import re
import sys


class Member:
    def __init__(self, name, phone):
        self.name = name
        if not re.fullmatch(r"09\d{9}", phone):
            raise ValueError("InvalidPhoneError")
        self.phone = phone

    def Research(self):
        a = "Research.txt" 
        with open       



        