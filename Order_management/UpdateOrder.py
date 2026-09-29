from .OrderManagement import OrderManagement


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

        order = self.get_order(order_id)

        if not order:
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
                item.get("quantity")
            )

        try:
            number = int(input("\nEnter item number to update: "))

            if number < 1 or number > len(order["items"]):
                raise ValueError

        except:
            self.save_error("Invalid order item number.")
            print("Invalid item number.")
            return

        item = order["items"][number - 1]

        print("\n1. Full")
        print("2. Half")

        size = input("Choose new size: ").strip()

        if size.lower() == "back":
            return

        menu_item = self.get_menu_item(item.get("item_id"))

        if not menu_item:
            print("Menu item no longer exists.")
            return

        if size == "1":
            item["size"] = "Full"
            item["price"] = menu_item["full"]
        elif size == "2":
            item["size"] = "Half"
            item["price"] = menu_item["half"]
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

        item["quantity"] = quantity

        self.save_orders(orders)
        self.log("Order updated: " + order_id)

        print("\nOrder updated successfully.")