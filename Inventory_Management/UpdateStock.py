import json
import os
from datetime import datetime


class UpdateStock:
    def __init__(self, file_path="data/inventory.json",
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

    def load_stock(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except:
            self.save_error("Unable to read inventory.json.")
            return []

    def save_stock(self, stock):
        with open(self.file_path, "w") as file:
            json.dump(stock, file, indent=4)

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

    def update_stock(self):
        stock = self.load_stock()

        print("\n========== UPDATE STOCK ==========")
        print("Type 'back' to return.")

        stock_id = input("Enter Stock ID: ").strip()

        if stock_id.lower() == "back":
            return

        if not stock_id.isdigit() or len(stock_id) != 10:
            self.save_error("Invalid stock ID.")
            print("Stock ID must contain exactly 10 digits.")
            return

        item = None

        for data in stock:
            if data.get("id") == stock_id:
                item = data
                break

        if item is None:
            self.save_error("Stock not found: " + stock_id)
            print("Stock item not found.")
            return

        print("Current Name:", item.get("name"))
        print("Current Quantity:", item.get("quantity"))

        name = input("New stock name: ").strip()

        if name.lower() == "back":
            return

        if not name:
            self.save_error("Empty stock name during update.")
            print("Stock name cannot be empty.")
            return

        try:
            quantity = int(input("New quantity: "))

            if quantity < 0:
                raise ValueError

        except:
            self.save_error("Invalid stock quantity during update.")
            print("Quantity cannot be negative.")
            return

        item["name"] = name
        item["quantity"] = quantity

        self.save_stock(stock)
        self.log("Stock updated: " + stock_id)

        print("\nStock updated successfully.")