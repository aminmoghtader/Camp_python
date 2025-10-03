import re
import sys
import os
import shutil
from datetime import datetime
import threading
import time


class Member:
    def __init__(self, name, phone):
        self.name = name
        if not re.fullmatch(r"09\d{9}", phone):
            raise ValueError("InvalidPhoneError")
        self.phone = phone

    def add_contact(self, section: str):

        filename = f"{section}.txt"
        with open(filename, "a+") as f:
            f.seek(0)
            lines = f.read().splitlines()
            for line in lines:
                if '|' in line:
                    _, ex_phone = line.split('|', 1)
                    if ex_phone == self.phone:
                        raise ValueError("PhoneAlreadyExists")
            f.write(f"{self.name}|{self.phone}\n")
            print(f"Contact {self.name} added to section {section}.\n--")


    @staticmethod
    def search(section:str, query:str ):

        filename = f"{section}.txt"
        q_lower = query.lower()
        results =[]

        try:
            with open(filename, "r") as f:
                for line in f:
                    if '|' in line:
                        name, phone = line.strip().split('|', 1)
                        if q_lower in name.lower:
                            results.append(name, phone)
        except FileNotFoundError:
            print(f"No contacts found in section {section}.")
            return []
        
        if results:
            print(f"Search results for {query} in {section}:\n")
            for idx, (name, phone) in enumerate(results,start=1):
                print(f"{idx}) {name} | {phone}")   
          
        else:
            print(f"No matching contacts found in section {section}.")
        return results
    
    @staticmethod
    def list(section:str):
        filename = f"{section}.txt"
        results = []

        try:
            with open(filename, "r") as f:
                for line in f:
                    if '|' in line:
                        name, phone = line.strip().split('|', 1)
                        results.append((name, phone))
        except FileNotFoundError:
            print(f"No contacts found in section {section}.")
            return []
        
        if results:
            print(f"Section {section} members:\n")
            for idx, (name, phone) in enumerate(results,start=1):
                print(f"{idx}) {name} | {phone}")   

        else:
            print(f"No matching contacts found in section {section}.")
        return results
    
    @staticmethod
    def all_list():
        filenames = ['Research.txt','Training.txt','Support.txt']
        results = []

        for filename in filenames:
            try:
                with open(filename, "r") as f:
                    for line in f:
                        if '|' in line:
                            name, phone = line.strip().split('|', 1)
                            results.append((name, phone))
            except FileNotFoundError:
                continue
    
        if results:
            print("All members:\n")
            for idx, (name, phone) in enumerate(results, start=1):
                print(f"{idx}) {name} | {phone}")
        else:
            print("No contacts found in any section.")

        return results


class Delete(Member):
    def __init__(self, name, phone):
        super().__init__(name, phone)

    def del_contact(self, section:str):
        filename = f"{section}.txt"
        with open(filename, "r") as f:
            lines = f.readlines()
        
        new = []
        deleted = 0
        for line in lines:
            if '|' in line:
                name, phone = line.strip().split('|', 1)
                if name == self.name:
                    deleted += 1
                    continue
                new.append(line)
        
        with open(filename, "w") as f:
            f.writelines(new)

        if deleted > 0:
            print(f"All contacts named {self.name} removed from section {section}.\n")
        else:
            print(f"No contact named {self.name} found in section {section}.")   


class Backup:
    auto_backup = False

    @staticmethod
    def run_backup():
        os.makedirs("backup", exist_ok=True)
        sections = ["Research.txt", "Training.txt", "Support.txt"]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        for file in sections:
            if os.path.exists(file):
                dst = os.path.join("backup", f"{file}_{timestamp}")
                shutil.copy(file, dst)
        print(f"Backup completed. Files saved in backup/ folder with timestamp {timestamp}.") 

    @staticmethod
    def Auto_backup(status: str):
        if status.upper() == "ON":
            Backup.auto_backup = True
            print("AutoBackup is ON") 
        elif status.upper() == "OFF":
            Backup.auto_backup = False
            print("AutoBackup is OFF")
        else:
            print("Invalid input. Use ON or OFF.")  

    @staticmethod
    def auto_run():
        while True:
            if Backup.auto_backup:
                Backup.run_backup()
            time.sleep(85000)

    @staticmethod
    def start_auto_backup():
        threading.Thread(target=Backup.auto_run, daemon=True).start()    

#####################################
def main():
    print("Guidance: add (Research/Training/Support) Ali 0912345678")
    print("exit for exiting the program")

    while True:
        try:
            choise = input(">> ").strip()
            parts = choise.split()

            if choise == "exit":
                sys.exit()

            elif len(parts) == 4 and parts[0].lower() == "add":
                s, n, p = parts[1], parts[2], parts[3]
                Member(n, p).add_contact(s)

            elif len(parts) == 2 and parts[0].lower() == "listsearch":
                s = parts[1]
                Member.list(s)   

            elif choise.lower() == "list all":
                Member.all_list()  

            else:
                print("Invalid input")

        except Exception as e:
            print("Error:", e)
            continue



        





if __name__ == "__main__":
    main()




    



    




















        
