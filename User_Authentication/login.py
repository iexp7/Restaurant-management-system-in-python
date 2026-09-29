import json
import os
import maskpass
from datetime import datetime


class Login:
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
            role + " login failed for username: " + username
        )
        self.log(role + " login failed: " + username)

        print("\nInvalid username or password.")
        return None

    def admin_login(self):
        return self.login("admin")

    def staff_login(self):
        return self.login("staff")