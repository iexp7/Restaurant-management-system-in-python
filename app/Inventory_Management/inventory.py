import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AddStock:
    def __init__(self, file_path=None, log_file=None, error_file=None):
        self.file_path = file_path or os.path.join(BASE_DIR, "database", "inventory.json")
        self.log_file = log_file or os.path.join(BASE_DIR, "logs", "velmora.log")
        self.error_file = error_file or os.path.join(BASE_DIR, "errors", "errors.json")
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


class UpdateStock:
    def __init__(self, file_path=None, log_file=None, error_file=None):
        self.file_path = file_path or os.path.join(BASE_DIR, "database", "inventory.json")
        self.log_file = log_file or os.path.join(BASE_DIR, "logs", "velmora.log")
        self.error_file = error_file or os.path.join(BASE_DIR, "errors", "errors.json")
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


class ViewStock:
    def __init__(self, file_path=None, log_file=None, error_file=None):
        self.file_path = file_path or os.path.join(BASE_DIR, "database", "inventory.json")
        self.log_file = log_file or os.path.join(BASE_DIR, "logs", "velmora.log")
        self.error_file = error_file or os.path.join(BASE_DIR, "errors", "errors.json")
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

    def view_stock(self):
        stock = self.load_stock()

        print("\n========== VELMORA INVENTORY ==========")

        if not stock:
            print("No stock available.")
            return

        valid_items = [item for item in stock if isinstance(item, dict)]
        invalid_items = len(stock) - len(valid_items)

        if invalid_items:
            self.save_error(
                f"Skipped {invalid_items} invalid inventory record(s).")
            print("Invalid stock entries were skipped.")

        if not valid_items:
            print("No stock available.")
            return

        categories = {}
        for item in valid_items:
            category = str(item.get("category", "Other")).strip().title()
            categories.setdefault(category or "Other", []).append(item)

        category_order = ["Asian", "Western", "Drinks"]
        category_order.extend(
            sorted(category for category in categories
                   if category not in category_order))

        for category in category_order:
            category_items = categories.get(category, [])
            if not category_items:
                continue

            print()
            print(f"============== {category.upper()} STOCK ==============")
            headers = ["ID", "ITEM", "QUANTITY"]
            rows = [
                [
                    str(item.get("id", "")),
                    str(item.get("name", "Unknown")),
                    str(item.get("quantity", 0))
                ]
                for item in category_items
            ]
            widths = [
                max(len(header), *(len(row[index]) for row in rows))
                for index, header in enumerate(headers)
            ]
            border = "+" + "+".join(
                "-" * (width + 2) for width in widths
            ) + "+"

            print(border)
            print(
                "| "
                + " | ".join(
                    f"{header:<{width}}"
                    for header, width in zip(headers, widths)
                )
                + " |")
            print(border)

            for row in rows:
                print(
                    "| "
                    + " | ".join(
                        f"{value:<{width}}"
                        for value, width in zip(row, widths)
                    )
                    + " |")

            print(border)

        self.log("Inventory viewed.")
