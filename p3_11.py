import re
import sys
import os
import shutil
from datetime import datetime
import threading
import time


class InvalidPhoneError(Exception):
    pass

class PhoneAlreadyExists(Exception):
    pass

class FileDoesNotExist(Exception):
    pass


class Member:
    def __init__(self, name, phone):
        self.name = name
        if not re.fullmatch(r"09\d{9}", phone):
            raise InvalidPhoneError("Error: Invalid phone number.")
        self.phone = phone

    def add_contact(self, section: str):
        filename = f"{section}.txt"
        if not os.path.exists(filename):
            open(filename, "w").close()  # create file if not exists

        with open(filename, "r+") as f:
            lines = f.read().splitlines()
            for line in lines:
                if '|' in line:
                    _, ex_phone = line.split('|', 1)
                    if ex_phone == self.phone:
                        raise PhoneAlreadyExists("Error: Phone number already exists in the section.")
            f.write(f"{self.name}|{self.phone}\n")
        print(f'Contact "{self.name}" added to section "{section}".')
        print("--")

    @staticmethod
    def search(section: str, query: str):
        filename = f"{section}.txt"
        q_lower = query.lower()
        results = []

        if not os.path.exists(filename):
            raise FileDoesNotExist(f"Error: Section {section} does not exist.")

        with open(filename, "r") as f:
            for line in f:
                if '|' in line:
                    name, phone = line.strip().split('|', 1)
                    if q_lower in name.lower():
                        results.append((name, phone))

        if results:
            print(f'Search results for "{query}" in "{section}":')
            for idx, (name, phone) in enumerate(results, start=1):
                print(f"{idx}) {name} | {phone}")
        else:
            print(f"No members found in section {section}.")
        print("--")
        return results

    @staticmethod
    def list(section: str):
        filename = f"{section}.txt"
        results = []

        if not os.path.exists(filename):
            raise FileDoesNotExist(f"Error: Section {section} does not exist.")

        with open(filename, "r") as f:
            for line in f:
                if '|' in line:
                    name, phone = line.strip().split('|', 1)
                    results.append((name, phone))

        if results:
            print(f"Section {section} members:")
            for idx, (name, phone) in enumerate(results, start=1):
                print(f"{idx}) {name} | {phone}")
        else:
            print(f"No members found in section {section}.")
        print("--")
        return results

    @staticmethod
    def all_list():
        filenames = ["Research.txt", "Training.txt", "Support.txt"]
        results = []

        for filename in filenames:
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    for line in f:
                        if '|' in line:
                            name, phone = line.strip().split('|', 1)
                            section_name = filename.replace(".txt","")
                            results.append((section_name, name, phone))

        if results:
            print("All members:")
            for idx, (section_name, name, phone) in enumerate(results, start=1):
                print(f"{idx}) {section_name} | {name} | {phone}")
        else:
            print("No members found in any section.")
        print("--")
        return results

    @staticmethod
    def del_contact(section: str, name_to_delete: str):
        filename = f"{section}.txt"
        if not os.path.exists(filename):
            raise FileDoesNotExist(f"Error: Section {section} does not exist.")

        with open(filename, "r") as f:
            lines = f.readlines()

        new_lines = []
        deleted_count = 0
        for line in lines:
            if '|' in line:
                name, phone = line.strip().split('|', 1)
                if name == name_to_delete:
                    deleted_count += 1
                    continue
            new_lines.append(line)

        with open(filename, "w") as f:
            f.writelines(new_lines)

        if deleted_count > 0:
            print(f'All contacts named "{name_to_delete}" removed from section "{section}".')
        else:
            print(f'No contact named "{name_to_delete}" found in section "{section}".')
        print("--")

# ==== Backup Class ====
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
        print("--")

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
        print("--")

    @staticmethod
    def auto_run():
        while True:
            if Backup.auto_backup:
                Backup.run_backup()
            time.sleep(85000)

    @staticmethod
    def start_auto_backup():
        threading.Thread(target=Backup.auto_run, daemon=True).start()

#############################################################
def main():

    Backup.start_auto_backup()

    while True:
        try:
            command = input(">> ").strip()
            parts = command.split()

            if command.lower() == "exit":
                sys.exit()

            elif command.lower() == "run backup":
                Backup.run_backup()

            elif command.lower().startswith("set autobackup"):
                if len(parts) == 3:
                    Backup.Auto_backup(parts[2])
                else:
                    print("Usage: set AutoBackup ON/OFF")
                    print("--")

            elif len(parts) >= 4 and parts[0].lower() == "add":
                section = parts[1]
                name = " ".join(parts[2:-1])
                phone = parts[-1]
                try:
                    Member(name, phone).add_contact(section)
                except (InvalidPhoneError, PhoneAlreadyExists) as e:
                    print(str(e))
                    print("--")

            elif len(parts) >= 3 and parts[0].lower() == "remove":
                section = parts[1]
                name = " ".join(parts[2:])
                try:
                    Member.del_contact(section, name)
                except FileDoesNotExist as e:
                    print(str(e))
                    print("--")

            elif len(parts) >= 3 and parts[0].lower() == "search":
                section = parts[1]
                name = " ".join(parts[2:])
                try:
                    Member.search(section, name)
                except FileDoesNotExist as e:
                    print(str(e))
                    print("--")

            elif len(parts) == 2 and parts[0].lower() == "listsearch":
                section = parts[1]
                try:
                    Member.list(section)
                except FileDoesNotExist as e:
                    print(str(e))
                    print("--")

            elif command.lower() == "list all":
                Member.all_list()

            else:
                print("Invalid input")
                print("--")

        except Exception as e:
            print("Error:", e)
            print("--")
            continue

if __name__ == "__main__":
    main()
