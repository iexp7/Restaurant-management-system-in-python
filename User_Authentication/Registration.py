import json
import os
import maskpass
from datetime import datetime


class Registration:
    def __init__(self, file_path="data/users.json",
                 log_file="logs/velmora.log",
                 error_file="errors/errors.json"):
        self.file_path = file_path
        self.log_file = log_file
        self.error_file = error_file
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
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                + " - " + message + "\n"
            )

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
            "role": "admin"
        }

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

        staff_id = str(1000000000 + len(users))

        while any(user.get("id") == staff_id for user in users):
            staff_id = str(int(staff_id) + 1)

        staff = {
            "id": staff_id,
            "username": username,
            "password": password,
            "role": "staff"
        }

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