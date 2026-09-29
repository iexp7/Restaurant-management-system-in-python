import json
import os
from datetime import datetime


class DeleteItem:
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

    def delete_item(self):
        items = self.load_items()

        print("\n===== DELETE MENU ITEM =====")
        print("Type 'back' to return.")

        item_id = input("Enter Item ID: ").strip()

        if item_id.lower() == "back":
            return

        if not item_id.isdigit() or len(item_id) != 10:
            self.save_error("Invalid menu item ID during delete.")
            print("Item ID must contain exactly 10 digits.")
            return

        for item in items:
            if item.get("id") == item_id:
                print("\nItem:", item.get("name"))
                confirm = input("Delete this item? (yes/no): ").strip().lower()

                if confirm == "back" or confirm == "no":
                    print("Delete cancelled.")
                    return

                if confirm != "yes":
                    self.save_error("Invalid delete confirmation.")
                    print("Enter yes or no.")
                    return

                items.remove(item)
                self.save_items(items)

                self.log("Menu item deleted: " + item_id)
                print("Item deleted successfully.")
                return

        self.save_error("Menu item not found: " + item_id)
        print("Item not found.")