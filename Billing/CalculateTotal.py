import json
import os
from datetime import datetime


class CalculateTotal:
    def __init__(self, order_file="data/orders.json",
                 log_file="logs/velmora.log",
                 error_file="errors/errors.json"):
        self.order_file = order_file
        self.log_file = log_file
        self.error_file = error_file
        self.create_files()

    def create_files(self):
        for path in [self.order_file, self.log_file, self.error_file]:
            folder = os.path.dirname(path)

            if folder and not os.path.exists(folder):
                os.makedirs(folder)

            if not os.path.exists(path):
                with open(path, "w") as file:
                    json.dump([], file) if path.endswith(".json") else file.write("")

    def load_orders(self):
        try:
            with open(self.order_file, "r") as file:
                return json.load(file)
        except:
            self.save_error("Unable to read orders.json.")
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

    def calculate(self, order_id):
        if not order_id.isdigit() or len(order_id) != 10:
            self.save_error("Invalid order ID for total calculation.")
            return None

        orders = self.load_orders()

        for order in orders:
            if order.get("id") == order_id:

                if order.get("status") != "Active":
                    self.save_error(
                        "Billing attempted for inactive order: " + order_id
                    )
                    print("Only active orders can be billed.")
                    return None

                total = 0

                for item in order.get("items", []):
                    total += item.get("price", 0) * item.get("quantity", 0)

                self.log("Total calculated for order: " + order_id)

                return total

        self.save_error("Order not found: " + order_id)
        print("Order not found.")
        return None