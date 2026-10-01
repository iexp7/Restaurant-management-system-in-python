import json
import os
from datetime import datetime


class Menu:
    def __init__(self, file_path="data/menu.json",
                 log_file="logs/velmora.log",
                 error_file="errors/errors.json"):
        self.file_path = file_path
        self.log_file = log_file
        self.error_file = error_file
        self.create_files()
        self.create_default_menu()

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

    def create_default_menu(self):
        items = self.load_items()

        if items:
            return

        items = [
            {
                "id": "2000000001",
                "name": "Chicken Biryani",
                "category": "Asian",
                "full": 220,
                "half": 130
            },
            {
                "id": "2000000002",
                "name": "Chicken Fried Rice",
                "category": "Asian",
                "full": 180,
                "half": 110
            },
            {
                "id": "2000000003",
                "name": "Veg Fried Rice",
                "category": "Asian",
                "full": 150,
                "half": 90
            },
            {
                "id": "2000000004",
                "name": "Hakka Noodles",
                "category": "Asian",
                "full": 160,
                "half": 95
            },
            {
                "id": "2000000005",
                "name": "Chilli Chicken",
                "category": "Asian",
                "full": 210,
                "half": 125
            },
            {
                "id": "2000000006",
                "name": "Chicken Manchurian",
                "category": "Asian",
                "full": 200,
                "half": 120
            },
            {
                "id": "2000000007",
                "name": "Paneer Tikka",
                "category": "Asian",
                "full": 190,
                "half": 115
            },
            {
                "id": "2000000008",
                "name": "Spring Rolls",
                "category": "Asian",
                "full": 140,
                "half": 85
            },
            {
                "id": "2000000009",
                "name": "Momos",
                "category": "Asian",
                "full": 130,
                "half": 80
            },
            {
                "id": "2000000010",
                "name": "Thai Noodles",
                "category": "Asian",
                "full": 180,
                "half": 110
            },
            {
                "id": "2000000011",
                "name": "Chicken Burger",
                "category": "Western",
                "full": 180,
                "half": 110
            },
            {
                "id": "2000000012",
                "name": "Veg Burger",
                "category": "Western",
                "full": 150,
                "half": 90
            },
            {
                "id": "2000000013",
                "name": "Chicken Pizza",
                "category": "Western",
                "full": 280,
                "half": 170
            },
            {
                "id": "2000000014",
                "name": "Margherita Pizza",
                "category": "Western",
                "full": 240,
                "half": 150
            },
            {
                "id": "2000000015",
                "name": "Pasta Alfredo",
                "category": "Western",
                "full": 220,
                "half": 135
            },
            {
                "id": "2000000016",
                "name": "Chicken Steak",
                "category": "Western",
                "full": 320,
                "half": 190
            },
            {
                "id": "2000000017",
                "name": "French Fries",
                "category": "Western",
                "full": 120,
                "half": 70
            },
            {
                "id": "2000000018",
                "name": "Garlic Bread",
                "category": "Western",
                "full": 130,
                "half": 80
            },
            {
                "id": "2000000019",
                "name": "Grilled Sandwich",
                "category": "Western",
                "full": 150,
                "half": 90
            },
            {
                "id": "2000000020",
                "name": "Chicken Wrap",
                "category": "Western",
                "full": 170,
                "half": 100
            }
        ]

        self.save_items(items)
        self.log("Default Velmora menu created.")

    def get_item(self, item_id):
        items = self.load_items()

        for item in items:
            if item.get("id") == item_id:
                return item

        self.save_error("Menu item not found: " + item_id)
        return None