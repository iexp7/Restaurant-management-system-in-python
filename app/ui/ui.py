from User_Authentication.Authentication import (Login, Admin,staff,Registration,User,)
from Menu_management.Menu import Menu, AddItem, ViewItem, UpdateItem, DeleteItem
from Order_management.OrderManagement import (CreateOrder,ViewOrder,UpdateOrder,CancelOrder,)
from Billing.billing import (CalculateTotal, Tax, Discount, GenerateBill,)
from Inventory_Management.inventory import (AddStock, ViewStock, UpdateStock,)
from Table_booking.TableBooking import (ViewTable,BookTable,CancelBooking,BookingStatus,)


class ui:
    def __init__(self):
        self.login = Login()
        self.admin = Admin()
        self.registration = Registration()
        self.registration.create_admin()
        self.menu = Menu()
        self.additem = AddItem()
        self.viewitem = ViewItem()
        self.updateitem = UpdateItem()
        self.deleteitem = DeleteItem()
        self.createorder = CreateOrder()
        self.vieworder = ViewOrder()
        self.updateorder = UpdateOrder()
        self.cancelorder = CancelOrder()
        self.calculatetotal = CalculateTotal()
        self.tax = Tax()
        self.discount = Discount()
        self.generatebill = GenerateBill()
        self.addstock = AddStock()
        self.viewstock = ViewStock()
        self.updatestock = UpdateStock()
        self.viewtable = ViewTable()
        self.booktable = BookTable()
        self.cancelbooking = CancelBooking()
        self.bookingstatus = BookingStatus()

    def start(self):
        while True:
            print("\n========== VELMORA, WELCOMES YOU :) ==========")
            print("1. Admin Login")
            print("2. Staff Login")
            print("3. Exit")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                self.admin_login()
            elif choice == "2":
                self.staff_login()
            elif choice == "3":
                print("\nThank you for visiting Velmora.")
                break
            else:
                self.login.save_error("Invalid main menu choice.")
                print("Invalid choice.")

    def admin_login(self):
        user = self.login.admin_login()
        if user:
            self.admin_menu(user)

    def staff_login(self):
        user = self.login.staff_login()
        if user:
            self.staff_menu(user)

    def admin_menu(self, user):
        while True:
            print("\n========== VELMORA ADMIN ==========")
            print("1. Staff Management")
            print("2. Menu Management")
            print("3. Order Management")
            print("4. Billing")
            print("5. Inventory Management")
            print("6. View Tables")
            print("7. Book Table")
            print("8. Cancel Booking")
            print("9. Booking Status")
            print("10. User Information")
            print("11. Back")
            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.admin.staff_management()
            elif choice == "2":
                self.menu_management()
            elif choice == "3":
                self.admin_order_management(user.get("id"))
            elif choice == "4":
                self.billing_menu()
            elif choice == "5":
                self.inventory_menu()
            elif choice == "6":
                self.viewtable.view_tables()
            elif choice == "7":
                self.book_table(user.get("id"))
            elif choice == "8":
                self.cancel_booking()
            elif choice == "9":
                self.bookingstatus.booking_status()
            elif choice == "10":
                User(user).show_user()
            elif choice == "11":
                break
            else:
                self.admin.save_error("Invalid admin menu choice.")
                print("Invalid choice.")

    def staff_menu(self, user):
        staff_logger = staff()
        while True:
            print("\n========== VELMORA STAFF ==========")
            print("Logged in:", user.get("username"))
            print("-----------------------------------")
            print("1. View Menu")
            print("2. New Order")
            print("3. View My Orders")
            print("4. Update My Order")
            print("5. Cancel My Order")
            print("6. Calculate Order Total")
            print("7. Generate Bill")
            print("8. View Stock")
            print("9. View Tables")
            print("10. Book Table")
            print("11. Cancel Booking")
            print("12. Booking Status")
            print("13. User Information")
            print("14. Back")
            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.viewitem.display_items()
            elif choice == "2":
                self.createorder.create_order(user.get("id"))
            elif choice == "3":
                self.vieworder.view_orders(user.get("id"))
            elif choice == "4":
                self.updateorder.update_order(user.get("id"))
            elif choice == "5":
                self.cancelorder.cancel_order(user.get("id"))
            elif choice == "6":
                self.calculate_order_total()
            elif choice == "7":
                self.generate_bill()
            elif choice == "8":
                self.viewstock.view_stock()
            elif choice == "9":
                self.viewtable.view_tables()
            elif choice == "10":
                self.booktable.book_table(user.get("id"))
            elif choice == "11":
                self.cancelbooking.cancel_booking(user.get("id"))
            elif choice == "12":
                self.bookingstatus.booking_status(user.get("id"))
            elif choice == "13":
                User(user).show_user()
            elif choice == "14":
                staff_logger.log("Staff logged out: " + user.get("username"))
                break
            else:
                staff_logger.save_error("Invalid staff menu choice.")
                print("Invalid choice.")

    def menu_management(self):
        while True:
            print("\n========== MENU MANAGEMENT ==========")
            print("1. Add Item")
            print("2. View Items")
            print("3. Update Item")
            print("4. Delete Item")
            print("5. Back")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                self.additem.add_item()
            elif choice == "2":
                self.viewitem.display_items()
            elif choice == "3":
                self.updateitem.update_item()
            elif choice == "4":
                self.deleteitem.delete_item()
            elif choice == "5":
                break
            else:
                self.admin.save_error("Invalid menu management choice.")
                print("Invalid choice.")

    def admin_order_management(self, admin_id):
        while True:
            print("\n========== ORDER MANAGEMENT ==========")
            print("1. New Order")
            print("2. View Orders")
            print("3. Update Order")
            print("4. Cancel Order")
            print("5. Calculate Total")
            print("6. Generate Bill")
            print("7. Back")
            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.createorder.create_order(admin_id, is_admin=True)
            elif choice == "2":
                self.vieworder.view_orders()
            elif choice == "3":
                self.updateorder.update_order()
            elif choice == "4":
                self.cancelorder.cancel_order()
            elif choice == "5":
                self.calculate_order_total()
            elif choice == "6":
                self.generate_bill()
            elif choice == "7":
                break
            else:
                self.admin.save_error("Invalid order management choice.")
                print("Invalid choice.")

    def billing_menu(self):
        while True:
            print("\n========== VELMORA BILLING ==========")
            print("1. Calculate Total")
            print("2. Calculate GST")
            print("3. Apply Discount")
            print("4. Generate Bill")
            print("5. Back")
            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.calculate_order_total()
            elif choice == "2":
                self.calculate_gst()
            elif choice == "3":
                self.calculate_discount()
            elif choice == "4":
                self.generate_bill()
            elif choice == "5":
                break
            else:
                self.admin.save_error("Invalid billing choice.")
                print("Invalid choice.")

    def calculate_order_total(self):
        print("\n========== CALCULATE TOTAL ==========")
        print("Type 'back' to return.")
        order_id = input("Enter Order ID: ").strip()

        if order_id.lower() == "back":
            return
        if not order_id.isdigit() or len(order_id) != 10:
            self.admin.save_error("Invalid order ID.")
            print("Order ID must contain exactly 10 digits.")
            return
        total = self.calculatetotal.calculate(order_id)

        if total is not None:
            print("\nOrder Subtotal: ₹", total)

    def calculate_gst(self):
        print("\n========== GST CALCULATION ==========")
        print("Type 'back' to return.")
        order_id = input("Enter Order ID: ").strip()

        if order_id.lower() == "back":
            return
        if not order_id.isdigit() or len(order_id) != 10:
            self.admin.save_error("Invalid order ID.")
            print("Order ID must contain exactly 10 digits.")
            return
        self.tax.calculate_tax(order_id)

    def calculate_discount(self):
        print("\n========== DISCOUNT ==========")
        print("Type 'back' to return.")
        order_id = input("Enter Order ID: ").strip()
        if order_id.lower() == "back":
            return
        if not order_id.isdigit() or len(order_id) != 10:
            self.admin.save_error("Invalid order ID.")
            print("Order ID must contain exactly 10 digits.")
            return
        self.discount.calculate_discount(order_id)

    def generate_bill(self):
        print("\n========== GENERATE BILL ==========")
        print("Type 'back' to return.")
        order_id = input("Enter Order ID: ").strip()

        if order_id.lower() == "back":
            return

        if not order_id.isdigit() or len(order_id) != 10:
            self.admin.save_error("Invalid order ID.")
            print("Order ID must contain exactly 10 digits.")
            return

        self.generatebill.generate_bill(order_id)

    def book_table(self, admin_id):
        print("\n========== BOOK TABLE ==========")
        print("Type 'back' to return.")
        if admin_id == "back":
            return

        if not str(admin_id).isdigit() or len(str(admin_id)) != 10:
            self.admin.save_error("Invalid admin ID for table booking.")
            print("Admin ID must contain exactly 10 digits.")
            return

        self.booktable.book_table(admin_id)

    def cancel_booking(self):
        print("\n========== CANCEL BOOKING ==========")
        self.cancelbooking.cancel_booking()

    def booking_status(self):
        print("\n========== BOOKING STATUS ==========")
        self.bookingstatus.booking_status()

    def inventory_menu(self):
        while True:
            print("\n========== INVENTORY MANAGEMENT ==========")
            print("1. Add Stock")
            print("2. View Stock")
            print("3. Update Stock")
            print("4. Back")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                self.addstock.add_stock()
            elif choice == "2":
                self.viewstock.view_stock()
            elif choice == "3":
                self.updatestock.update_stock()
            elif choice == "4":
                break
            else:
                self.admin.save_error("Invalid inventory choice.")
                print("Invalid choice.")
