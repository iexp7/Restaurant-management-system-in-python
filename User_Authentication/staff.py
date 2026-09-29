import os
import json
from datetime import datetime


class Waitstaff:
    def __init__(self, log_file="logs/velmora.log",
                 error_file="errors/errors.json"):
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
                self.log(
                    "Staff selected option " + choice +
                    ": " + staff.get("username")
                )
            else:
                self.save_error("Invalid staff menu choice.")
                print("Invalid choice. Please try again.")