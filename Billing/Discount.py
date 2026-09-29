from Billing.Tax import Tax


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