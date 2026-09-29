from Billing.CalculateTotal import CalculateTotal
from datetime import datetime


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