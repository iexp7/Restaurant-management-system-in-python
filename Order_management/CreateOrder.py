from .OrderManagement import OrderManagement
from datetime import datetime


class CreateOrder(OrderManagement):

    def create_order(self, staff_id):
        orders = self.load_orders()

        print("\n========== NEW ORDER ==========")
        print("Type 'back' to return.")

        items = []

        while True:
            item_id = input("\nEnter Item ID: ").strip()

            if item_id.lower() == "back":
                return

            if not item_id.isdigit() or len(item_id) != 10:
                self.save_error("Invalid menu item ID.")
                print("Item ID must contain exactly 10 digits.")
                continue

            item = self.get_menu_item(item_id)

            if not item:
                print("Item not found.")
                continue

            print("\nItem:", item["name"])
            print("1. Full - ₹", item["full"])
            print("2. Half - ₹", item["half"])

            size = input("Choose size: ").strip()

            if size == "1":
                size_name = "Full"
                price = item["full"]
            elif size == "2":
                size_name = "Half"
                price = item["half"]
            elif size.lower() == "back":
                return
            else:
                self.save_error("Invalid food size.")
                print("Choose 1 or 2.")
                continue

            try:
                quantity = int(input("Enter quantity: "))

                if quantity <= 0:
                    raise ValueError

            except:
                self.save_error("Invalid order quantity.")
                print("Quantity must be greater than 0.")
                continue

            items.append({
                "item_id": item["id"],
                "name": item["name"],
                "size": size_name,
                "price": price,
                "quantity": quantity
            })

            print("Item added to order.")

            more = input("Add another item? (yes/no): ").strip().lower()

            if more == "no":
                break

            if more != "yes":
                self.save_error("Invalid add-item choice.")
                print("Enter yes or no.")
                break

        if not items:
            print("No items added.")
            return

        order_id = self.generate_order_id(orders)

        order = {
            "id": order_id,
            "staff_id": staff_id,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Active",
            "items": items
        }

        orders.append(order)
        self.save_orders(orders)

        self.log("New order created: " + order_id)

        print("\n========== ORDER CREATED ==========")
        print("Order ID:", order_id)
        print("Status:", "Active")
        print("Items:", len(items))
        print("Order created successfully.")