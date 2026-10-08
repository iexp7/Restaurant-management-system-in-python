import json
import os
import maskpass
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Registration:
    def __init__(self, file_path=None, log_file=None, error_file=None):
        self.file_path = file_path or os.path.join(BASE_DIR, "database", "users.json")
        self.log_file = log_file or os.path.join(BASE_DIR, "logs", "velmora.log")
        self.error_file = error_file or os.path.join(BASE_DIR, "errors", "errors.json")
        self.create_files()

    def create_files(self):
        for file_path in [self.file_path, self.log_file, self.error_file]:
            folder = os.path.dirname(file_path)

            if folder and not os.path.exists(folder):
                os.makedirs(folder)

            if not os.path.exists(file_path):
                with open(file_path, "w") as file:
                    if file_path.endswith(".json"):
                        json.dump([], file)
                    else:
                        file.write("")

    def load_users(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except:
            self.save_error("users.json could not be read.")
            return []

    def save_users(self, users):
        with open(self.file_path, "w") as file:
            json.dump(users, file, indent=4)

    def save_error(self, message):
        try:
            with open(self.error_file, "r") as file:
                errors = json.load(file)
        except:
            errors = []

        errors.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": message
        })

        with open(self.error_file, "w") as file:
            json.dump(errors, file, indent=4)

    def log(self, message):
        with open(self.log_file, "a") as file:
            file.write(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")+ " - " + message + "\n")

    def admin_exists(self, users):
        for user in users:
            if user.get("role") == "admin":
                return True
        return False

    def create_admin(self):
        users = self.load_users()

        if self.admin_exists(users):
            print("\nAdmin already exists.")
            return

        admin = {
            "id": "1000000001",
            "username": "bhupendra",
            "password": "291769",
            "role": "admin"}

        users.append(admin)
        self.save_users(users)
        self.log("Admin account created.")

        print("\nVelmora Admin created successfully.")

    def add_staff(self):
        users = self.load_users()

        username = input("\nEnter staff username: ").strip()

        if username.lower() == "back":
            return

        if not username:
            self.save_error("Empty staff username entered.")
            print("Username cannot be empty.")
            return

        for user in users:
            if user.get("username") == username:
                self.save_error("Duplicate staff username: " + username)
                print("Username already exists.")
                return

        password = maskpass.askpass("Enter staff password: ")

        if not password:
            self.save_error("Empty staff password entered.")
            print("Password cannot be empty.")
            return

        staff_count = sum(1 for user in users if user.get("role") == "staff")
        staff_id = str(1000000001 + staff_count)

        while any(user.get("id") == staff_id for user in users):
            staff_id = str(int(staff_id) + 1)

        staff = {
            "id": staff_id,
            "username": username,
            "password": password,
            "role": "staff"}

        users.append(staff)
        self.save_users(users)
        self.log("Staff account created: " + username)

        print("\nStaff created successfully.")
        print("Staff ID:", staff_id)

    def register(self):
        users = self.load_users()

        if not self.admin_exists(users):
            self.create_admin()

        while True:
            print("\n===== VELMORA REGISTRATION =====")
            print("1. Add Staff")
            print("2. Back")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.add_staff()
            elif choice == "2":
                break
            else:
                self.save_error("Invalid registration menu choice.")
                print("Invalid choice. Please try again.")


class Login:
    def __init__(self, file_path=None, log_file=None, error_file=None):
        self.file_path = file_path or os.path.join(BASE_DIR, "database", "users.json")
        self.log_file = log_file or os.path.join(BASE_DIR, "logs", "velmora.log")
        self.error_file = error_file or os.path.join(BASE_DIR, "errors", "errors.json")
        self.create_files()

    def create_files(self):
        for path in [self.file_path, self.log_file, self.error_file]:
            folder = os.path.dirname(path)

            if folder and not os.path.exists(folder):
                os.makedirs(folder)

            if not os.path.exists(path):
                with open(path, "w") as file:
                    if path.endswith(".json"):
                        json.dump([], file)
                    else:
                        file.write("")

    def load_users(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except:
            self.save_error("Unable to read users.json.")
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
            file.write(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                + " - " + message + "\n")

    def login(self, role):
        users = self.load_users()

        print("\n===== VELMORA " + role.upper() + " LOGIN =====")
        print("Type 'back' to return.")

        username = input("Username: ").strip()

        if username.lower() == "back":
            return None

        if not username:
            self.save_error("Empty username entered during login.")
            print("Username cannot be empty.")
            return None

        password = maskpass.askpass("Password: ")

        if not password:
            self.save_error("Empty password entered during login.")
            print("Password cannot be empty.")
            return None

        for user in users:
            if (user.get("username") == username and
                    user.get("password") == password and
                    user.get("role") == role):

                self.log(role + " login successful: " + username)
                print("\nLogin successful.")
                return user

        self.save_error(
            role + " login failed for username: " + username)
        
        self.log(role + " login failed: " + username)

        print("\nInvalid username or password.")
        return None

    def admin_login(self):
        return self.login("admin")

    def staff_login(self):
        return self.login("staff")


class Admin:
    def __init__(self, file_path=None, log_file=None, error_file=None):
        self.file_path = file_path or os.path.join(BASE_DIR, "database", "users.json")
        self.log_file = log_file or os.path.join(BASE_DIR, "logs", "velmora.log")
        self.error_file = error_file or os.path.join(BASE_DIR, "errors", "errors.json")
        self.create_files()

    def create_files(self):
        for path in [self.file_path, self.log_file, self.error_file]:
            folder = os.path.dirname(path)

            if folder and not os.path.exists(folder):
                os.makedirs(folder)

            if not os.path.exists(path):
                with open(path, "w") as file:
                    json.dump([], file) if path.endswith(".json") else file.write("")

    def load_users(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except:
            self.save_error("Unable to read users.json.")
            return []

    def save_users(self, users):
        with open(self.file_path, "w") as file:
            json.dump(users, file, indent=4)

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
            file.write(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                + " - " + message + "\n")

    def view_staff(self):
        users = self.load_users()

        print("\n===== VELMORA STAFF =====")

        found = False

        for user in users:
            if user.get("role") == "staff":
                found = True
                print("ID:", user.get("id"))
                print("Username:", user.get("username"))
                print("-" * 25)

        if not found:
            print("No staff found.")

    def remove_staff(self):
        users = self.load_users()

        staff_id = input("\nEnter Staff ID: ").strip()

        if staff_id.lower() == "back":
            return

        if not staff_id.isdigit() or len(staff_id) != 10:
            self.save_error("Invalid staff ID entered.")
            print("Staff ID must contain exactly 10 digits.")
            return

        for user in users:
            if user.get("id") == staff_id and user.get("role") == "staff":
                users.remove(user)
                self.save_users(users)

                self.log("Staff removed: " + staff_id)
                print("Staff removed successfully.")
                return

        self.save_error("Staff ID not found: " + staff_id)
        print("Staff not found.")

    def staff_management(self):

        registration = Registration()

        while True:
            print("\n===== STAFF MANAGEMENT =====")
            print("1. Add Staff")
            print("2. View Staff")
            print("3. Remove Staff")
            print("4. Back")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                registration.add_staff()
            elif choice == "2":
                self.view_staff()
            elif choice == "3":
                self.remove_staff()
            elif choice == "4":
                break
            else:
                self.save_error("Invalid staff management choice.")
                print("Invalid choice.")

    def admin_menu(self):
        while True:
            print("\n========== VELMORA ADMIN ==========")
            print("1. Staff Management")
            print("2. Back")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.staff_management()
            elif choice == "2":
                break
            else:
                self.save_error("Invalid admin menu choice.")
                print("Invalid choice.")


class staff:
    def __init__(self, log_file=None, error_file=None):
        self.log_file = log_file or os.path.join(BASE_DIR, "logs", "velmora.log")
        self.error_file = error_file or os.path.join(BASE_DIR, "errors", "errors.json")
        self.create_files()

    def create_files(self):
        for path in [self.log_file, self.error_file]:
            folder = os.path.dirname(path)

            if folder and not os.path.exists(folder):
                os.makedirs(folder)

            if not os.path.exists(path):
                with open(path, "w") as file:
                    json.dump([], file) if path.endswith(".json") else file.write("")

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
            file.write(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                + " - " + message + "\n")

    def staff_menu(self, staff):
        while True:
            print("\n========== VELMORA STAFF ==========")
            print("Logged in:", staff.get("username"))
            print("-----------------------------------")
            print("1. View Menu")
            print("2. New Order")
            print("3. View Order")
            print("4. Update Order")
            print("5. Cancel Order")
            print("6. View Stock")
            print("7. View Tables")
            print("8. Book Table")
            print("9. Cancel Booking")
            print("10. Booking Status")
            print("11. Back")

            choice = input("Enter choice: ").strip()

            if choice == "11":
                self.log("Staff logged out: " + staff.get("username"))
                break

            if choice in ["1", "2", "3", "4", "5",
                          "6", "7", "8", "9", "10"]:
                print("\nThis option will be connected with its module.")
                self.log("Staff selected option " + choice +": " + staff.get("username"))
            else:
                self.save_error("Invalid staff menu choice.")
                print("Invalid choice. Please try again.")


staff = staff


class User:
    def __init__(self, user=None, log_file=None, error_file=None):
        self.user = user or {}
        self.log_file = log_file or os.path.join(BASE_DIR, "logs", "velmora.log")
        self.error_file = error_file or os.path.join(BASE_DIR, "errors", "errors.json")
        self.create_files()

    def create_files(self):
        for path in [self.log_file, self.error_file]:
            folder = os.path.dirname(path)

            if folder and not os.path.exists(folder):
                os.makedirs(folder)

            if not os.path.exists(path):
                with open(path, "w") as file:
                    json.dump([], file) if path.endswith(".json") else file.write("")

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

    def get_id(self):
        return self.user.get("id")

    def get_username(self):
        return self.user.get("username")

    def get_role(self):
        return self.user.get("role")

    def is_admin(self):
        return self.get_role() == "admin"

    def is_staff(self):
        return self.get_role() == "staff"

    def show_user(self):
        print("\n===== USER INFORMATION =====")
        print("ID:", self.get_id())
        print("Username:", self.get_username())
        print("Role:", self.get_role())
