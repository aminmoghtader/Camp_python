import re
import sys

def validate_time(func):
    def wrapper(self, *args, **kwargs):
        for k, v in zip(func.__code__.co_varnames[1:], args):
            if 'hour' in k:
                if not (0 <= v <= 23):
                    print("INvalid")
                    return
            elif 'minute' in k:
                if not (0 <= v <= 59):
                    print("invalid")
                    return
            elif 'miladi_day' in k or 'shamsi_day' in k:
                if not (1 <= v <= 30):
                    print("invalid")
                    return
            elif 'miladi_month_num' in k or 'shamsi_month_num' in k:
                if not (1 <= v <= 12):
                    print("Invalid input")
                    return
            elif 'miladi_year' in k or 'shamsi_year' in k:
                if v <= 0:
                    print("Invalid input")
                    return
        return func(self, *args, **kwargs)
    return wrapper                


class Time:  
    def __init__(self, hour=0, minute=0):
        self._hour = hour
        self._minute = minute
    @property
    def hour(self):
        return self._hour
    @property
    def minute(self):
        return self._minute
    @validate_time
    def Change(self, hour, minute):
        self._hour = hour
        self._minute = minute
    def __str__(self):
        return f"{self._hour:02d}:{self._minute:02d}"    

class Day(Time):
    def __init__(self,miladi_day=1, shamsi_day=1, hour=0, minute=0):
        super().__init__(hour, minute)
        self._miladi_day = miladi_day
        self._shamsi_day = shamsi_day        

    @property
    def miladi_day(self):
        return self._miladi_day
    @property
    def shamsi_day(self):
        return self._shamsi_day
    @validate_time
    def Change(self, miladi_day, shamsi_day):
        self._miladi_day = miladi_day
        self._shamsi_day = shamsi_day
    def __str__(self):
        return f"{self._miladi_day:02d}/{self._shamsi_day:02d} {super().__str__()}"

class Month(Day):
    def __init__(self, miladi_month_name="January", shamsi_month_name="Farvardin", 
                 miladi_month_num=1, shamsi_month_num=1, miladi_day=1, 
                 shamsi_day=1, hour=0, minute=0):
        super().__init__(miladi_day, shamsi_day, hour, minute)
        self._miladi_month_name = miladi_month_name
        self._shamsi_month_name = shamsi_month_name
        self._miladi_month_num = miladi_month_num
        self._shamsi_month_num = shamsi_month_num
    @property
    def miladi_month_name(self):
        return self._miladi_month_name
    @property
    def shamsi_month_name(self):
        return self._shamsi_month_name
    @property        
    def miladi_month_num(self):
        return self._shamsi_month_name
    @property
    def shamsi_month_num(self):
        return self._shamsi_month_num
    @validate_time
    def Change(self, miladi_month_num, shamsi_month_num, miladi_month_name, 
               shamsi_month_name):
        self._miladi_month_num = miladi_month_num
        self._shamsi_month_num = shamsi_month_num
        self._miladi_month_name = miladi_month_name
        self._shamsi_month_name = shamsi_month_name
    def __str__(self):
        return f"{self._miladi_month_name}/{self._shamsi_month_name} {self._miladi_day:02d}/{self._shamsi_day:02d} {super().__str__()}"
    
class Calendar(Month):
    def __init__(self, cal_id, name, miladi_year=2024, shamsi_year=1403, 
                 miladi_month_name="January", shamsi_month_name="Farvardin", 
                 miladi_month_num=1, shamsi_month_num=1, miladi_day=1, 
                 shamsi_day=1, hour=0, minute=0):
        super().__init__(miladi_month_name, shamsi_month_name, miladi_month_num, 
                         shamsi_month_num, miladi_day, shamsi_day, hour, minute)
        self._id = cal_id 
        self._name = name
        self._miladi_year = miladi_year
        self._shamsi_year = shamsi_year
        self.events = []
        self.enabled = False   
    @property
    def id(self):
        return self._id
    @property
    def name(self):
        return self._name
    @property
    def miladi_year(self):
        return self._miladi_year
    @property
    def shamsi_year(self):
        return self._shamsi_year
    @validate_time
    def Change(self, miladi_year=None, shamsi_year=None, name=None):
        if miladi_year is not None:
            self._miladi_year = miladi_year
        if shamsi_year is not None:
            self._shamsi_year = shamsi_year
        if name is not None:
            self._name = name
    def __str__(self):
        return f"{self._id} {self._name}: Calendar"

class Event:
    def __init__(self, title, type_event, miladi_date, shamsi_date, 
                 hour=0, minute=0):
        self._title = title
        self._type = type_event
        self.miladi_date = miladi_date
        self.shamsi_date = shamsi_date
        self._hour = hour
        self._minute = minute 
    @property
    def title(self):
        return self._title
    @property
    def type_event(self):
        return self._type
    def __str__(self):
        return f"Event {self._title}: {self._type}"

users = {}
current_user = None
cal_id_counter = 1

def valid_username(u):
    return re.fullmatch(r"[A-Za-z0-9_]+", u)
def valid_pass(p):
    if len(p) < 5: return False
    if not re.fullmatch(r"[A-Z]", p): return False
    if not re.fullmatch(r"[a-z]", p): return False
    if not re.fullmatch(r"[0-9]", p): return False
    return True

        
    
        

        
