import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CalculateTotal:
    def __init__(self, order_file=None, log_file=None, error_file=None):
        self.order_file = order_file or os.path.join(BASE_DIR, "database", "orders.json")
        self.log_file = log_file or os.path.join(BASE_DIR, "logs", "velmora.log")
        self.error_file = error_file or os.path.join(BASE_DIR, "errors", "errors.json")
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
            "message": message})

        with open(self.error_file, "w") as file:
            json.dump(errors, file, indent=4)

    def log(self, message):
        with open(self.log_file, "a") as file:
            file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+ " - " + message + "\n")

    def calculate(self, order_id):
        if not order_id.isdigit() or len(order_id) != 10:
            self.save_error("Invalid order ID for total calculation.")
            return None

        orders = self.load_orders()

        for order in orders:
            if order.get("id") == order_id:

                if order.get("status") != "Active":
                    self.save_error("Billing attempted for inactive order: " + order_id)
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


class Tax(CalculateTotal):
    def calculate_tax(self, order_id):
        total = self.calculate(order_id)

        if total is None:
            return None

        tax = total * 0.05
        final_total = total + tax

        self.log("5% GST calculated for order: " + order_id)

        print("\n========== GST ==========")
        print("Subtotal : ₹", round(total, 2))
        print("GST 5%   : ₹", round(tax, 2))
        print("Total    : ₹", round(final_total, 2))

        return {
            "subtotal": round(total, 2),
            "gst": round(tax, 2),
            "total": round(final_total, 2)
        }


class Discount(Tax):
    def calculate_discount(self, order_id):
        total = self.calculate(order_id)

        if total is None:
            return None

        print("\n========== DISCOUNT ==========")
        print("Enter 0 for no discount.")

        try:
            discount = float(input("Discount (%): "))

            if discount < 0 or discount > 100:
                raise ValueError

        except:
            self.save_error("Invalid discount percentage.")
            print("Discount must be between 0 and 100.")
            return None

        discount_amount = total * discount / 100
        after_discount = total - discount_amount

        gst = after_discount * 0.05
        final_total = after_discount + gst

        self.log("Discount calculated for order: " + order_id)

        print("\nSubtotal       : ₹", round(total, 2))
        print("Discount       : ₹", round(discount_amount, 2))
        print("After Discount : ₹", round(after_discount, 2))
        print("GST 5%         : ₹", round(gst, 2))
        print("Final Total    : ₹", round(final_total, 2))

        return {
            "subtotal": round(total, 2),
            "discount_percent": discount,
            "discount": round(discount_amount, 2),
            "after_discount": round(after_discount, 2),
            "gst": round(gst, 2),
            "total": round(final_total, 2)
        }


class GenerateBill(Discount):
    def __init__(self, bill_file=None, log_file=None, error_file=None):
        super().__init__(log_file=log_file, error_file=error_file)
        self.bill_file = bill_file or os.path.join(BASE_DIR, "database", "bills.json")
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

        orders_file = self.order_file

        try:

            with open(orders_file, "r") as file:
                orders = json.load(file)

        except:

            self.save_error("Unable to read orders.json.")
            return

        order = None

        for item in orders:

            if item.get("id") == order_id:
                order = item
                break

        if order is None:

            print("Order not found.")
            return

        if order.get("status") == "Complete":

            print("Bill has already been generated.")
            return

        payment = input("\nPayment (Cash/Card/Online): ").strip()

        if payment.lower() == "back":
            return

        if payment.lower() not in ["cash", "card", "online"]:

            self.save_error("Invalid payment method.")
            print("Payment must be Cash, Card, or Online.")
            return

        bills = self.load_bills()

        bill_id = str(4000000000 + len(bills) + 1)

        while any(
            bill.get("id") == bill_id
            for bill in bills
        ):
            bill_id = str(int(bill_id) + 1)

        bill = {
            "id": bill_id,
            "order_id": order_id,
            "order_type": order.get(
                "order_type",
                "Dine-in" if order.get("booking_id") else "Not recorded"),
            "booking_id": order.get("booking_id"),
            "table_id": order.get("table_id"),
            "customer_name": order.get("customer_name"),
            "customer_phone": order.get("customer_phone"),
            "people": order.get("people"),
            "items": [
                {
                    **item,
                    "line_total": round(
                        item.get("price", 0) * item.get("quantity", 0), 2)
                }
                for item in order.get("items", [])
            ],
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

        order["status"] = "Complete"

        with open(orders_file, "w") as file:
            json.dump(orders, file, indent=4)

        bookings_file = os.path.join(BASE_DIR, "database", "bookings.json")
        booking_id = str(order.get("booking_id", "")).strip()
        table_id = str(order.get("table_id", "")).strip()
        if booking_id:
            with open(bookings_file, "r") as file:
                bookings = json.load(file)

            booking = next(
                (
                    item for item in bookings
                    if str(item.get("id", "")).strip() == booking_id), None)

            if booking is None:
                self.save_error(
                    "Booking not found for completed bill: " + booking_id)
                print("Warning: booking status could not be updated.")
            else:
                booking["status"] = "Complete"
                table_id = str(booking.get("table_id", table_id)).strip()

                with open(bookings_file, "w") as file:
                    json.dump(bookings, file, indent=4)

            if booking is not None and table_id:
                tables_file = os.path.join(BASE_DIR, "database", "tables.json")
                with open(tables_file, "r") as file:
                    tables = json.load(file)

                table = next(
                    (
                        item for item in tables
                        if str(item.get("id", "")).strip() == table_id), None)

                if table is None:
                    self.save_error(
                        "Table not found for completed booking: " + table_id)
                    print("Warning: table availability could not be updated.")
                else:
                    table["status"] = "Available"

                    with open(tables_file, "w") as file:
                        json.dump(tables, file, indent=4)
            elif booking is not None:
                self.save_error("Completed booking has no table ID: " + booking_id)
                print("Warning: table availability could not be updated.")

        self.log("Bill generated: " + bill_id)

        print("\n========== VELMORA BILL ==========")
        print("Bill ID        :", bill_id)
        print("Order ID       :", order_id)
        print("Order Type     :", bill["order_type"])
        print("Date           :", bill["date"])
        print("Customer Name  :", order.get("customer_name"))
        print("Customer Phone :", order.get("customer_phone") or "Not provided")
        if booking_id:
            print("Booking ID     :", booking_id)
            print("Table ID       :", table_id)
            print("People         :", order.get("people") or "Not recorded")
        print("\nItems:")
        print(
            f"{'Item':<24} {'ID':<12} {'Size':<10} "
            f"{'Qty':>5} {'Unit Price':>12} {'Line Total':>12}")
        print("-" * 81)
        for item in bill["items"]:
            print(
                f"{str(item.get('name', 'Unknown')):<24} "
                f"{str(item.get('item_id', '')):<12} "
                f"{str(item.get('size', '')):<10} "
                f"{item.get('quantity', 0):>5} "
                f"₹{item.get('price', 0):>11.2f} "
                f"₹{item.get('line_total', 0):>11.2f}")
        print("-" * 81)
        print("Subtotal       : ₹", result["subtotal"])
        print("Discount       : ₹", result["discount"])
        print("GST 5%         : ₹", result["gst"])
        print("Final Total    : ₹", result["total"])
        print("Payment        :", payment.title())
        print("==================================")
        print("Bill generated successfully.")
