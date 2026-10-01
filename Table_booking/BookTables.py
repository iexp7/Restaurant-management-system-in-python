import json
import os
from datetime import datetime


class BookTable:
    def __init__(self, table_file="data/tables.json",
                 booking_file="data/bookings.json",
                 log_file="logs/velmora.log",
                 error_file="errors/errors.json"):
        self.table_file = table_file
        self.booking_file = booking_file
        self.log_file = log_file
        self.error_file = error_file
        self.create_files()

    def create_files(self):
        for path in [
            self.table_file,
            self.booking_file,
            self.log_file,
            self.error_file]:
            folder = os.path.dirname(path)

            if folder and not os.path.exists(folder):
                os.makedirs(folder)

            if not os.path.exists(path):
                with open(path, "w") as file:
                    json.dump([], file) if path.endswith(".json") else file.write("")

    def load_tables(self):
        try:
            with open(self.table_file, "r") as file:
                return json.load(file)
        except:
            self.save_error("Unable to read tables.json.")
            return []

    def save_tables(self, tables):
        with open(self.table_file, "w") as file:
            json.dump(tables, file, indent=4)

    def load_bookings(self):
        try:
            with open(self.booking_file, "r") as file:
                return json.load(file)
        except:
            self.save_error("Unable to read bookings.json.")
            return []

    def save_bookings(self, bookings):
        with open(self.booking_file, "w") as file:
            json.dump(bookings, file, indent=4)

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

    def book_table(self, staff_id):
        tables = self.load_tables()
        bookings = self.load_bookings()

        print("\n========== BOOK TABLE ==========")
        print("Type 'back' to return.")

        table_id = input("Enter Table ID: ").strip()

        if table_id.lower() == "back":
            return

        if not table_id.isdigit() or len(table_id) != 10:
            self.save_error("Invalid table ID.")
            print("Table ID must contain exactly 10 digits.")
            return

        table = None

        for item in tables:
            if item.get("id") == table_id:
                table = item
                break

        if table is None:
            self.save_error("Table not found: " + table_id)
            print("Table not found.")
            return

        if table.get("status") == "Booked":
            print("This table is already booked.")
            return

        name = input("Customer name: ").strip()

        if name.lower() == "back":
            return

        if not name:
            self.save_error("Empty customer name.")
            print("Customer name cannot be empty.")
            return

        try:
            people = int(input("Number of people: "))

            if people <= 0:
                raise ValueError

        except:
            self.save_error("Invalid number of people.")
            print("Number of people must be greater than 0.")
            return

        booking_id = str(7000000000 + len(bookings) + 1)

        while any(
            booking.get("id") == booking_id for booking in bookings):
            booking_id = str(int(booking_id) + 1)

        booking = {
            "id": booking_id,
            "table_id": table_id,
            "staff_id": staff_id,
            "customer_name": name,
            "people": people,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Active"
        }

        bookings.append(booking)

        table["status"] = "Booked"

        self.save_bookings(bookings)
        self.save_tables(tables)

        self.log("Table booked: " + table_id)

        print("\n========== BOOKING SUCCESSFUL ==========")
        print("Booking ID :", booking_id)
        print("Table ID   :", table_id)
        print("Customer   :", name)
        print("People     :", people)
        print("Status     : Active")