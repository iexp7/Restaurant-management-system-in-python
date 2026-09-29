import json
import os
from datetime import datetime


class User:
    def __init__(self, user=None,
                 log_file="logs/velmora.log",
                 error_file="errors/errors.json"):
        self.user = user or {}
        self.log_file = log_file
        self.error_file = error_file
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