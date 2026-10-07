import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class OrderManagement:
    def __init__(self, file_path=None, menu_file=None, log_file=None, error_file=None):
        self.file_path = file_path or os.path.join(BASE_DIR, "database", "orders.json")
        self.menu_file = menu_file or os.path.join(BASE_DIR, "database", "menu.json")
        self.inventory_file = os.path.join(BASE_DIR, "database", "inventory.json")
        self.log_file = log_file or os.path.join(BASE_DIR, "logs", "velmora.log")
        self.error_file = error_file or os.path.join(BASE_DIR, "errors", "errors.json")
        self.create_files()

    def create_files(self):
        for path in [
            self.file_path,
            self.menu_file,
            self.inventory_file,
            self.log_file,
            self.error_file
        ]:

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

    def load_inventory(self):
        with open(self.inventory_file, "r") as file:
            return json.load(file)

    def save_inventory(self, inventory):
        with open(self.inventory_file, "w") as file:
            json.dump(inventory, file, indent=4)

    def change_inventory(self, items, quantity_change):
        inventory = self.load_inventory()
        changes = {}

        for order_item in items:
            item_id = str(order_item.get("item_id", ""))
            item_name = order_item.get("name", "")
            stock_index = next(
                (index for index, stock_item in enumerate(inventory)
                    if str(stock_item.get("id", "")) == item_id),None)

            if stock_index is None:
                stock_index = next(
                    (
                        index for index, stock_item in enumerate(inventory)
                        if stock_item.get("name", "").casefold()
                        == item_name.casefold()),None)

            if stock_index is None:
                self.save_error("Inventory item not found: " + item_name)
                print("No stock item found for " + item_name + ".")
                return False

            stock_item = inventory[stock_index]
            current_quantity = stock_item.get("quantity")
            if (
                not isinstance(current_quantity, int)
                or isinstance(current_quantity, bool)
                or current_quantity < 0):

                self.save_error("Invalid inventory quantity: " + item_name)
                print("Stock quantity is not set for " + item_name + ".")
                return False

            ordered_quantity = order_item.get("quantity")
            if (
                not isinstance(ordered_quantity, int)
                or isinstance(ordered_quantity, bool)
                or ordered_quantity <= 0):

                self.save_error("Invalid order quantity: " + item_name)
                print("Invalid order quantity for " + item_name + ".")
                return False

            updated_quantity = (current_quantity+ changes.get(stock_index, 0)+ quantity_change * ordered_quantity)
            
            if updated_quantity < 0:
                self.save_error("Insufficient stock: " + item_name)
                print("Not enough stock available for " + item_name + ".")
                return False

            changes[stock_index] = updated_quantity - current_quantity

        for index, change in changes.items():
            inventory[index]["quantity"] += change

        self.save_inventory(inventory)
        return True

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

        errors.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"message": message})

        with open(self.error_file, "w") as file:
            json.dump(errors, file, indent=4)

    def log(self, message):
        with open(self.log_file, "a") as file:
            file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+ " - " + message + "\n")

    def generate_order_id(self, orders=None):
        orders = self.load_orders() if orders is None else orders
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


class CreateOrder(OrderManagement):

    def create_order(self, staff_id, is_admin=False):

        print("\n========== NEW ORDER ==========")
        print("Type 'back' to return.")

        print("1. Dine-in")
        print("2. Takeaway")
        order_choice = input("Choose order type: ").strip()

        if order_choice.lower() == "back":
            return

        if order_choice not in ("1", "2"):
            self.save_error("Invalid order type.")
            print("Choose 1 for dine-in or 2 for takeaway.")
            return

        order_type = "Dine-in" if order_choice == "1" else "Takeaway"
        booking = None
        booking_id = None
        customer_name = None
        customer_phone = None
        people = None

        if order_type == "Dine-in":
            booking_id = input("Enter Booking ID: ").strip()

            if booking_id.lower() == "back":
                return

            if not booking_id.isdigit() or len(booking_id) != 10:
                self.save_error("Invalid booking ID.")
                print("Booking ID must contain exactly 10 digits.")
                return

            booking_file = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "database",
                "bookings.json"
            )

            try:
                with open(booking_file, "r") as file:
                    bookings = json.load(file)
            except:
                self.save_error("Unable to read bookings.json.")
                print("Booking data not found.")
                return

            booking = next(
                (item for item in bookings if item.get("id") == booking_id),
                None)

            if booking is None:
                self.save_error("Booking not found.")
                print("Booking not found.")
                return

            if booking.get("status") != "Active":
                print("Booking is not active.")
                return

            if not is_admin and booking.get("staff_id") != staff_id:
                print("You can only create an order for your booking.")
                return

            customer_name = str(booking.get("customer_name", "")).strip()
            customer_phone = str(booking.get("customer_phone", "")).strip()
            people = booking.get("people")

            if not customer_phone:
                customer_phone = input("Enter Customer Phone (10 digits): ").strip()
                if customer_phone.lower() == "back":
                    return
                if not customer_phone.isdigit() or len(customer_phone) != 10:
                    self.save_error("Invalid customer phone number.")
                    print("Customer phone must contain exactly 10 digits.")
                    return

                booking["customer_phone"] = customer_phone
                with open(booking_file, "w") as file:
                    json.dump(bookings, file, indent=4)
        else:
            customer_name = input("Enter Customer Name: ").strip()
            if customer_name.lower() == "back":
                return
            if not customer_name:
                self.save_error("Invalid customer name for takeaway order.")
                print("Customer name cannot be empty.")
                return

            customer_phone = input("Enter Customer Phone (10 digits): ").strip()
            if customer_phone.lower() == "back":
                return
            if not customer_phone.isdigit() or len(customer_phone) != 10:
                self.save_error("Invalid customer phone number.")
                print("Customer phone must contain exactly 10 digits.")
                return

        menu = self.load_menu()

        if not menu:

            print("Menu is empty.")
            return

        items = []

        while True:

            categories = {}
            for menu_item in menu:
                if not isinstance(menu_item, dict):
                    continue
                category = str(
                    menu_item.get("category", "Other")).strip().title()
                categories.setdefault(category or "Other", []).append(menu_item)

            category_order = ["Asian", "Western", "Drinks"]
            category_order.extend(
                sorted(
                    category for category in categories
                    if category not in category_order))

            for category in category_order:
                category_items = categories.get(category, [])
                if not category_items:
                    continue

                print(f"\n============== {category.upper()} MENU ==============")

                if category == "Drinks":
                    headers = ["ID", "DRINK", "PRICE"]
                    rows = [
                        [
                            str(menu_item.get("id", "")),
                            str(menu_item.get("name", "Unknown")),
                            "Rs." + str(menu_item.get("price", 0))
                        ]
                        for menu_item in category_items
                    ]
                else:
                    headers = ["ID", "FOOD ITEM", "OPTION", "PRICE"]
                    rows = []
                    for menu_item in category_items:
                        item_id = str(menu_item.get("id", ""))
                        name = str(menu_item.get("name", "Unknown"))
                        full_price = menu_item.get(
                            "full_price", menu_item.get("full", 0))
                        half_price = menu_item.get(
                            "half_price", menu_item.get("half", 0))
                        rows.extend([
                            [item_id, name, "Full", "Rs." + str(full_price)],
                            ["", "", "Half", "Rs." + str(half_price)]
                        ])

                widths = [
                    max(len(header), *(len(row[index]) for row in rows))
                    for index, header in enumerate(headers)
                ]
                border = "+" + "+".join(
                    "-" * (width + 2) for width in widths) + "+"

                print(border)
                print(
                    "| "
                    + " | ".join(
                        f"{header:<{width}}"
                        for header, width in zip(headers, widths))
                    + " |")
                print(border)

                for row in rows:
                    print(
                        "| "
                        + " | ".join(
                            f"{value:<{width}}"
                            for value, width in zip(row, widths))
                        + " |")

                print(border)

            print("\nType 'back' to finish order.")

            item_id = input("Enter Item ID: ").strip()

            if item_id.lower() == "back":

                if not items:
                    print("No items selected. Order not created.")
                    return

                break

            if not item_id.isdigit() or len(item_id) != 4:

                self.save_error("Invalid item ID.")
                print("Menu item IDs must contain exactly 4 digits.")
                continue

            item = self.get_menu_item(item_id)

            if item is None:

                self.save_error("Menu item not found.")
                print("Item not found.")
                continue

            is_drink = str(item.get("category", "")).strip().casefold() == "drinks"

            if is_drink:
                size = "Regular"
            else:
                size = input("Enter Size (Full/Half): ").strip()

                if size.lower() == "back":
                    if not items:
                        print("No items selected. Order not created.")
                        return
                    break

                if size.lower() not in ["full", "half"]:

                    self.save_error("Invalid food size.")
                    print("Size must be Full or Half.")
                    continue

            quantity = input("Enter Quantity: ").strip()

            if quantity.lower() == "back":
                if not items:
                    print("No items selected. Order not created.")
                    return
                break

            if not quantity.isdigit() or int(quantity) <= 0:

                self.save_error("Invalid quantity.")
                print("Quantity must be greater than 0.")
                continue

            if is_drink:
                price = item.get("price", 0)
            elif size.lower() == "full":

                price = item.get("full_price", item.get("full", 0))

            else:

                price = item.get("half_price", item.get("half", 0))

            items.append({
                "item_id": item.get("id"),
                "name": item.get("name"),
                "size": size.title(),
                "price": price,
                "quantity": int(quantity)})

            print("Item added successfully.")

        orders = self.load_orders()

        order_id = self.generate_order_id(orders)

        order = {
            "id": order_id,
            "order_type": order_type,
            "customer_name": customer_name,
            "customer_phone": customer_phone,
            "staff_id": staff_id,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Active",
            "items": items}

        if booking is not None:
            order["booking_id"] = booking_id
            order["table_id"] = booking.get("table_id")
            order["people"] = people

        if not self.change_inventory(items, -1):
            return

        order["inventory_deducted"] = True
        orders.append(order)

        self.save_orders(orders)

        self.log("Order created: " + order_id)

        print("\nOrder created successfully.")
        print("Order ID:", order_id)
        print("Order Type:", order_type)
        print("Customer:", customer_name)
        if booking is not None:
            print("Booking ID:", booking_id)
            print("Table ID:", booking.get("table_id"))


class ViewOrder(OrderManagement):

    def view_orders(self, staff_id=None):
        orders = self.load_orders()

        print("\n========== VELMORA ORDERS ==========")

        found = False

        for order in orders:

            if staff_id and order.get("staff_id") != staff_id:
                continue

            found = True

            print("\nOrder ID :", order.get("id"))
            print(
                "Order Type :", order.get(
                    "order_type",
                    "Dine-in" if order.get("booking_id") else "Not recorded"))
            print("Customer   :", order.get("customer_name") or "Not recorded")
            print("Phone      :", order.get("customer_phone") or "Not recorded")
            if order.get("booking_id"):
                print("Booking ID :", order.get("booking_id"))
                print("Table ID   :", order.get("table_id") or "Not recorded")
                print("People     :", order.get("people") or "Not recorded")
            print("Staff ID :", order.get("staff_id"))
            print("Date     :", order.get("date"))
            print("Status   :", order.get("status"))

            print("Items:")

            widths = [12, 24, 10, 8, 10, 10]
            headers = ["ITEM ID", "FOOD ITEM", "OPTION", "QTY", "PRICE", "TOTAL"]
            border = "+" + "+".join(
                "-" * (width + 2)
                for width in widths
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

            for item in order.get("items", []):
                total = item.get("price", 0) * item.get("quantity", 0)
                price_text = "Rs." + str(item.get("price", 0))
                total_text = "Rs." + str(total)

                print(
                    f"| {str(item.get('item_id', '')):<{widths[0]}}"
                    f" | {str(item.get('name', 'Unknown')):<{widths[1]}}"
                    f" | {str(item.get('size', '')):<{widths[2]}}"
                    f" | {str(item.get('quantity', 0)):<{widths[3]}}"
                    f" | {price_text:<{widths[4]}}"
                    f" | {total_text:<{widths[5]}} |")

            print(border)

        if not found:
            print("No orders found.")
            return

        if staff_id is None:
            self.update_order_status(orders)

        self.log("Orders viewed.")

    def update_order_status(self, orders):
        update = input("\nUpdate an order status? (yes/no): ").strip().lower()

        if update in ("no", "back"):
            return

        if update != "yes":
            self.save_error("Invalid order status update choice.")
            print("Enter yes or no.")
            return

        order_id = input("Enter Order ID: ").strip()

        if not order_id.isdigit() or len(order_id) != 10:
            self.save_error("Invalid order ID during status update.")
            print("Order ID must contain exactly 10 digits.")
            return

        order = next(
            (order for order in orders if order.get("id") == order_id),None)

        if not order:
            self.save_error("Order not found during status update: " + order_id)
            print("Order not found.")
            return

        print("\n1. Pending")
        print("2. Completed")
        print("3. Cancelled")
        status_choice = input("Choose new status: ").strip()

        statuses = {
            "1": "Pending",
            "2": "Completed",
            "3": "Cancelled"}
        status = statuses.get(status_choice)

        if not status:
            self.save_error("Invalid order status selection.")
            print("Choose 1, 2, or 3.")
            
            return

        order["status"] = status
        self.save_orders(orders)
        self.log("Order status updated: " + order_id + " - " + status)
        print("Order status updated to " + status + ".")


class UpdateOrder(OrderManagement):

    def update_order(self, staff_id=None):
        orders = self.load_orders()

        print("\n========== UPDATE ORDER ==========")
        print("Type 'back' to return.")

        order_id = input("Enter Order ID: ").strip()

        if order_id.lower() == "back":
            return

        if not order_id.isdigit() or len(order_id) != 10:
            self.save_error("Invalid order ID.")
            print("Order ID must contain exactly 10 digits.")
            return

        order = next(
            (item for item in orders if item.get("id") == order_id),
            None)

        if not order:
            self.save_error("Order not found: " + order_id)
            print("Order not found.")
            return

        if staff_id and order.get("staff_id") != staff_id:
            self.save_error("Staff tried to update another staff order.")
            print("You can update only your own order.")
            return

        if order.get("status") != "Active":
            print("Only active orders can be updated.")
            return

        print("\nCurrent Items:")

        for i, item in enumerate(order.get("items", []), 1):
            print(
                i, ".",
                item.get("name"),
                "|",
                item.get("size"),
                "| Qty:",
                item.get("quantity"))

        try:
            number = int(input("\nEnter item number to update: "))

            if number < 1 or number > len(order["items"]):
                raise ValueError

        except:
            self.save_error("Invalid order item number.")
            print("Invalid item number.")
            return

        item = order["items"][number - 1]

        menu_item = self.get_menu_item(item.get("item_id"))

        if not menu_item:
            print("Menu item no longer exists.")
            return

        if str(menu_item.get("category", "")).strip().casefold() == "drinks":
            item["size"] = "Regular"
            item["price"] = menu_item.get("price", 0)
        else:
            print("\n1. Full")
            print("2. Half")

            size = input("Choose new size: ").strip()

            if size.lower() == "back":
                return

            if size == "1":
                item["size"] = "Full"
                item["price"] = menu_item.get("full_price", menu_item.get("full", 0))
            elif size == "2":
                item["size"] = "Half"
                item["price"] = menu_item.get("half_price", menu_item.get("half", 0))
            else:
                self.save_error("Invalid order size.")
                print("Choose 1 or 2.")
                return

        try:
            quantity = int(input("Enter new quantity: "))

            if quantity <= 0:
                raise ValueError

        except:
            self.save_error("Invalid order quantity.")
            print("Quantity must be greater than 0.")
            return

        if order.get("inventory_deducted"):
            quantity_change = item["quantity"] - quantity
            if quantity_change and not self.change_inventory(
                [dict(item, quantity=abs(quantity_change))],
                1 if quantity_change > 0 else -1):
                return

        item["quantity"] = quantity

        self.save_orders(orders)
        self.log("Order updated: " + order_id)

        print("\nOrder updated successfully.")


class CancelOrder(OrderManagement):

    def cancel_order(self, staff_id=None):
        orders = self.load_orders()

        print("\n========== CANCEL ORDER ==========")
        print("Type 'back' to return.")

        order_id = input("Enter Order ID: ").strip()

        if order_id.lower() == "back":
            return

        if not order_id.isdigit() or len(order_id) != 10:
            self.save_error("Invalid order ID during cancellation.")
            print("Order ID must contain exactly 10 digits.")
            return

        order = next(
            (item for item in orders if item.get("id") == order_id),None)

        if not order:
            self.save_error("Order not found: " + order_id)
            print("Order not found.")
            return

        if staff_id and order.get("staff_id") != staff_id:
            self.save_error("Staff tried to cancel another staff order.")
            print("You can cancel only your own order.")
            return

        if order.get("status") == "Cancelled":
            print("Order is already cancelled.")
            return

        confirm = input("Cancel this order? (yes/no): ").strip().lower()

        if confirm == "back" or confirm == "no":
            print("Cancellation cancelled.")
            return

        if confirm != "yes":
            self.save_error("Invalid cancellation confirmation.")
            print("Enter yes or no.")
            return

        if order.get("inventory_deducted"):
            if not self.change_inventory(order.get("items", []), 1):
                return
            order["inventory_deducted"] = False

        order["status"] = "Cancelled"

        self.save_orders(orders)
        self.log("Order cancelled: " + order_id)

        print("\nOrder cancelled successfully.")
