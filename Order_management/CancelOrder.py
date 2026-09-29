from .OrderManagement import OrderManagement


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

        order = self.get_order(order_id)

        if not order:
            print("Order not found.")
            return

        if staff_id and order.get("staff_id") != staff_id:
            self.save_error(
                "Staff tried to cancel another staff order."
            )
            print("You can cancel only your own order.")
            return

        if order.get("status") == "Cancelled":
            print("Order is already cancelled.")
            return

        confirm = input(
            "Cancel this order? (yes/no): "
        ).strip().lower()

        if confirm == "back" or confirm == "no":
            print("Cancellation cancelled.")
            return

        if confirm != "yes":
            self.save_error("Invalid cancellation confirmation.")
            print("Enter yes or no.")
            return

        order["status"] = "Cancelled"

        self.save_orders(orders)
        self.log("Order cancelled: " + order_id)

        print("\nOrder cancelled successfully.")