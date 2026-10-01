import json
import os
from datetime import datetime


class ViewItem:
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

    def view_items(self):
        items = self.load_items()

        if not items:
            print("\nNo menu items available.")
            return

        print("\n================ VELMORA MENU ================")

        for item in items:
            print("\nID       :", item.get("id"))
            print("Name     :", item.get("name"))
            print("Category :", item.get("category"))
            print("Full     : ₹", item.get("full"))
            print("Half     : ₹", item.get("half"))
            print("-----------------------------------------------")

        self.log("Menu items viewed.")