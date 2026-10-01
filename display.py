from User_Authentication.login import Login
from User_Authentication.admin import Admin
from User_Authentication.staff import Waitstaff
from User_Authentication.Registration import Registration
from User_Authentication.user import User

from Menu_management.Menu import Menu
from Menu_management.AddItem import AddItem
from Menu_management.ViewItem import ViewItem
from Menu_management.UpdateItem import UpdateItem
from Menu_management.DeleteItem import DeleteItem

from Order_management.CreateOrder import CreateOrder
from Order_management.viewOrder import ViewOrder
from Order_management.UpdateOrder import UpdateOrder
from Order_management.CancelOrder import CancelOrder

from Billing.CalculateTotal import CalculateTotal
from Billing.Tax import Tax
from Billing.Discount import Discount
from Billing.generateBill import GenerateBill

from Inventory_Management.AddStock import AddStock
from Inventory_Management.ViewStock import ViewStock
from Inventory_Management.UpdateStock import UpdateStock

from Table_booking.Viewtables import ViewTables
from Table_booking.BookTables import BookTable


class Display:
    def __init__(self):
        self.login = Login()
        self.admin = Admin()
        self.registration = Registration()
        self.registration.create_admin()
        Menu()
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
        self.viewtable = ViewTables()
        self.booktable = BookTable()

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
            print("8. User Information")
            print("9. Back")
            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.admin.staff_management()
            elif choice == "2":
                self.menu_management()
            elif choice == "3":
                self.admin_order_management()
            elif choice == "4":
                self.billing_menu()
            elif choice == "5":
                self.inventory_menu()
            elif choice == "6":
                self.viewtable.view_tables()
            elif choice == "7":
                self.book_table()
            elif choice == "8":
                User(user).show_user()
            elif choice == "9":
                break
            else:
                self.admin.save_error("Invalid admin menu choice.")
                print("Invalid choice.")

    def staff_menu(self, user):
        staff = Waitstaff()
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
            print("11. User Information")
            print("12. Back")
            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.viewitem.view_items()
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
                User(user).show_user()
            elif choice == "12":
                staff.log("Staff logged out: " + user.get("username"))
                break
            else:
                staff.save_error("Invalid staff menu choice.")
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
                self.viewitem.view_items()
            elif choice == "3":
                self.updateitem.update_item()
            elif choice == "4":
                self.deleteitem.delete_item()
            elif choice == "5":
                break
            else:
                self.admin.save_error("Invalid menu management choice.")
                print("Invalid choice.")

    def admin_order_management(self):
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
                staff_id = input("Enter Staff ID: ").strip()
                if staff_id.lower() == "back":
                    continue
                if not staff_id.isdigit() or len(staff_id) != 10:
                    self.admin.save_error("Invalid staff ID.")
                    print("Staff ID must contain exactly 10 digits.")
                    continue
                self.createorder.create_order(staff_id)
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

    def book_table(self):
        print("\n========== BOOK TABLE ==========")
        print("Type 'back' to return.")
        staff_id = input("Enter Staff ID: ").strip()
        if staff_id.lower() == "back":
            return
        if not staff_id.isdigit() or len(staff_id) != 10:
            self.admin.save_error("Invalid staff ID.")
            print("Staff ID must contain exactly 10 digits.")
            return
        self.booktable.book_table(staff_id)

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