import json
import os
from datetime import datetime


class OrderManagement:
    def __init__(self, file_path="data/orders.json",
                 menu_file="data/menu.json",
                 log_file="logs/velmora.log",
                 error_file="errors/errors.json"):
        self.file_path = file_path
        self.menu_file = menu_file
        self.log_file = log_file
        self.error_file = error_file
        self.create_files()

    def create_files(self):
        for path in [self.file_path, self.menu_file,self.log_file, self.error_file]:

            folder = os.path.dirname(path)

            if folder and not os.path.exists(folder):
                os.makedirs(folder)

            if not os.path.exists(path):
                with open(path, "w") as file:
                    if path.endswith(".json"):
                        json.dump([], file)
                    else:
                        file.write("")

    def load_orders(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except:
            self.save_error("Unable to read orders.json.")
            return []

    def save_orders(self, orders):
        with open(self.file_path, "w") as file:
            json.dump(orders, file, indent=4)

    def load_menu(self):
        try:
            with open(self.menu_file, "r") as file:
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

    def generate_order_id(self, orders):
        number = 3000000001

        if orders:
            numbers = [
                int(order["id"]) for order in orders
                if order.get("id", "").isdigit()]

            if numbers:
                number = max(numbers) + 1

        return str(number)

    def get_menu_item(self, item_id):
        menu = self.load_menu()

        for item in menu:
            if item.get("id") == item_id:
                return item

        self.save_error("Menu item not found: " + item_id)
        return None

    def get_order(self, order_id):
        orders = self.load_orders()

        for order in orders:
            if order.get("id") == order_id:
                return order

        self.save_error("Order not found: " + order_id)
        return None