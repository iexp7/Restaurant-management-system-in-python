import json
import os
from datetime import datetime


class AddStock:
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

    def add_stock(self):
        stock = self.load_stock()

        print("\n========== ADD STOCK ==========")
        print("Type 'back' to return.")

        name = input("Stock name: ").strip()

        if name.lower() == "back":
            return

        if not name:
            self.save_error("Empty stock name.")
            print("Stock name cannot be empty.")
            return

        for item in stock:
            if item.get("name", "").lower() == name.lower():
                self.save_error("Duplicate stock item: " + name)
                print("Stock item already exists.")
                return

        try:
            quantity = int(input("Quantity: "))

            if quantity <= 0:
                raise ValueError

        except:
            self.save_error("Invalid stock quantity.")
            print("Quantity must be greater than 0.")
            return

        stock_id = str(5000000000 + len(stock) + 1)

        while any(item.get("id") == stock_id for item in stock):
            stock_id = str(int(stock_id) + 1)

        item = {
            "id": stock_id,
            "name": name,
            "quantity": quantity
        }

        stock.append(item)
        self.save_stock(stock)

        self.log("Stock added: " + stock_id)

        print("\nStock added successfully.")
        print("Stock ID:", stock_id)