import json
import os
from datetime import datetime


class AddItem:
    def __init__(self, file_path="data/menu.json",
                 log_file="logs/velmora.log",
                 error_file="errors/errors.json"):
        self.file_path = file_path
        self.log_file = log_file
        self.error_file = error_file
        self.create_files()

    def create_files(self):
        for path in [self.file_path, self.log_file, self.error_file]:
            folder = os.path.dirname(path)

            if folder and not os.path.exists(folder):
                os.makedirs(folder)

            if not os.path.exists(path):
                with open(path, "w") as file:
                    json.dump([], file) if path.endswith(".json") else file.write("")

    def load_items(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except:
            self.save_error("Unable to read menu.json.")
            return []

    def save_items(self, items):
        with open(self.file_path, "w") as file:
            json.dump(items, file, indent=4)

    def save_error(self, message):
        try:
            with open(self.error_file, "r") as file:
                errors = json.load(file)
        except:
            errors = []

        errors.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": message})

        with open(self.error_file, "w") as file:
            json.dump(errors, file, indent=4)

    def log(self, message):
        with open(self.log_file, "a") as file:
            file.write(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                + " - " + message + "\n")

    def add_item(self):
        items = self.load_items()

        print("\n===== ADD MENU ITEM =====")
        print("Type 'back' at any time to return.")

        name = input("Item name: ").strip()

        if name.lower() == "back":
            return

        if not name:
            self.save_error("Empty item name.")
            print("Item name cannot be empty.")
            return

        for item in items:
            if item.get("name", "").lower() == name.lower():
                self.save_error("Duplicate menu item: " + name)
                print("Item already exists.")
                return

        category = input("Category (Asian/Western): ").strip()

        if category.lower() == "back":
            return

        if category.lower() not in ["asian", "western"]:
            self.save_error("Invalid food category.")
            print("Category must be Asian or Western.")
            return

        try:
            full = float(input("Full price: "))

            if full <= 0:
                raise ValueError

            half = float(input("Half price: "))

            if half <= 0 or half >= full:
                raise ValueError

        except:
            self.save_error("Invalid menu price entered.")
            print("Enter valid prices. Half price must be less than Full price.")
            return

        item_id = str(2000000000 + len(items) + 1)

        while any(item.get("id") == item_id for item in items):
            item_id = str(int(item_id) + 1)

        item = {
            "id": item_id,
            "name": name,
            "category": category.title(),
            "full": full,
            "half": half
        }

        items.append(item)
        self.save_items(items)

        self.log("Menu item added: " + name)

        print("\nItem added successfully.")
        print("Item ID:", item_id)