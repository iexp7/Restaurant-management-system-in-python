import json
import os
from datetime import datetime
from Billing.Discount import Discount


class GenerateBill(Discount):

    def __init__(self, bill_file="data/bills.json",
                 log_file="logs/velmora.log",
                 error_file="errors/errors.json"):
        super().__init__(log_file=log_file, error_file=error_file)
        self.bill_file = bill_file
        self.create_bill_file()

    def create_bill_file(self):
        folder = os.path.dirname(self.bill_file)

        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        if not os.path.exists(self.bill_file):
            with open(self.bill_file, "w") as file:
                json.dump([], file)

    def load_bills(self):
        try:
            with open(self.bill_file, "r") as file:
                return json.load(file)
        except:
            self.save_error("Unable to read bills.json.")
            return []

    def save_bills(self, bills):
        with open(self.bill_file, "w") as file:
            json.dump(bills, file, indent=4)

    def generate_bill(self, order_id):
        print("\n========== VELMORA BILL ==========")
        print("Type 'back' to return.")

        if not order_id.isdigit() or len(order_id) != 10:
            self.save_error("Invalid order ID for bill.")
            print("Order ID must contain exactly 10 digits.")
            return

        result = self.calculate_discount(order_id)

        if result is None:
            return

        payment = input("\nPayment (Card/Online): ").strip()

        if payment.lower() == "back":
            return

        if payment.lower() not in ["card", "online"]:
            self.save_error("Invalid payment method.")
            print("Payment must be Card or Online.")
            return

        bills = self.load_bills()

        bill_id = str(4000000000 + len(bills) + 1)

        while any(bill.get("id") == bill_id for bill in bills):
            bill_id = str(int(bill_id) + 1)

        bill = {
            "id": bill_id,
            "order_id": order_id,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "subtotal": result["subtotal"],
            "discount_percent": result["discount_percent"],
            "discount": result["discount"],
            "gst": result["gst"],
            "total": result["total"],
            "payment": payment.title()
        }

        bills.append(bill)
        self.save_bills(bills)

        self.log("Bill generated: " + bill_id)

        print("\n========== VELMORA BILL ==========")
        print("Bill ID        :", bill_id)
        print("Order ID       :", order_id)
        print("Subtotal       : ₹", result["subtotal"])
        print("Discount       : ₹", result["discount"])
        print("GST 5%         : ₹", result["gst"])
        print("Final Total    : ₹", result["total"])
        print("Payment        :", payment.title())
        print("==================================")
        print("Bill generated successfully.")