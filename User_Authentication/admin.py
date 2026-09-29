import json
import os
from datetime import datetime


class Admin:
    def __init__(self, file_path="data/users.json",
                 log_file="logs/velmora.log",
                 error_file="errors/errors.json"):
        self.file_path = file_path
        self.log_file = log_file
        self.error_file = error_file
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
            "message": message
        })

        with open(self.error_file, "w") as file:
            json.dump(errors, file, indent=4)

    def log(self, message):
        with open(self.log_file, "a") as file:
            file.write(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                + " - " + message + "\n"
            )

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
        from .Registration import Registration

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