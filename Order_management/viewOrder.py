from .OrderManagement import OrderManagement


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
            print("Staff ID :", order.get("staff_id"))
            print("Date     :", order.get("date"))
            print("Status   :", order.get("status"))

            print("Items:")

            for item in order.get("items", []):
                total = item.get("price", 0) * item.get("quantity", 0)

                print(
                    "  ",
                    item.get("name"),
                    "|",
                    item.get("size"),
                    "| Qty:",
                    item.get("quantity"),
                    "| ₹",
                    total
                )

            print("-" * 40)

        if not found:
            print("No orders found.")
            return

        self.log("Orders viewed.")