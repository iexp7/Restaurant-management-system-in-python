import json
import os
from datetime import datetime


class UpdateItem:
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
            "message": message
        })

        with open(self.error_file, "w") as file:
            json.dump(errors, file, indent=4)

    def log(self, message):
        with open(self.log_file, "a") as file:
            file.write(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                + " - " + message + "\n"
            )

    def update_item(self):
        items = self.load_items()

        print("\n===== UPDATE MENU ITEM =====")
        print("Type 'back' to return.")

        item_id = input("Enter Item ID: ").strip()

        if item_id.lower() == "back":
            return

        if not item_id.isdigit() or len(item_id) != 10:
            self.save_error("Invalid menu item ID.")
            print("Item ID must contain exactly 10 digits.")
            return

        item = None

        for data in items:
            if data.get("id") == item_id:
                item = data
                break

        if item is None:
            self.save_error("Menu item not found: " + item_id)
            print("Item not found.")
            return

        name = input("New name: ").strip()

        if name.lower() == "back":
            return

        if not name:
            self.save_error("Empty item name during update.")
            print("Name cannot be empty.")
            return

        category = input("Category (Asian/Western): ").strip()

        if category.lower() == "back":
            return

        if category.lower() not in ["asian", "western"]:
            self.save_error("Invalid category during menu update.")
            print("Category must be Asian or Western.")
            return

        try:
            full = float(input("New Full price: "))
            half = float(input("New Half price: "))

            if full <= 0 or half <= 0 or half >= full:
                raise ValueError

        except:
            self.save_error("Invalid price during menu update.")
            print("Invalid price. Half price must be less than Full price.")
            return

        item["name"] = name
        item["category"] = category.title()
        item["full"] = full
        item["half"] = half

        self.save_items(items)
        self.log("Menu item updated: " + item_id)

        print("\nMenu item updated successfully.")