import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class BookTable:

    def __init__(
        self,
        table_file=None,
        booking_file=None,
        log_file=None,
        error_file=None):
        
        self.table_file = table_file or os.path.join(BASE_DIR, "database", "tables.json")
        self.booking_file = booking_file or os.path.join(BASE_DIR, "database", "bookings.json")
        self.log_file = log_file or os.path.join(BASE_DIR, "logs", "velmora.log")
        self.error_file = error_file or os.path.join(BASE_DIR, "errors", "errors.json")
        self.create_files()

    def create_files(self):

        for file_path in [
            self.table_file,
            self.booking_file,
            self.log_file,
            self.error_file]:
            folder = os.path.dirname(file_path)

            if folder and not os.path.exists(folder):
                os.makedirs(folder)

            if not os.path.exists(file_path):

                if file_path.endswith(".json"):
                    with open(file_path, "w") as file:
                        json.dump([], file, indent=4)

                else:
                    with open(file_path, "w") as file:
                        file.write("")

    def load_tables(self):

        try:
            with open(self.table_file, "r") as file:
                return json.load(file)

        except:
            return []

    def save_tables(self, tables):

        with open(self.table_file, "w") as file:
            json.dump(tables, file, indent=4)

    def load_bookings(self):

        try:
            with open(self.booking_file, "r") as file:
                return json.load(file)

        except:
            return []

    def save_bookings(self, bookings):

        with open(self.booking_file, "w") as file:
            json.dump(bookings, file, indent=4)

    def save_error(self, message):

        errors = []

        try:
            with open(self.error_file, "r") as file:
                errors = json.load(file)

        except:
            errors = []

        errors.append({
            "error": message,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

        with open(self.error_file, "w") as file:
            json.dump(errors, file, indent=4)

    def log(self, message):

        with open(self.log_file, "a") as file:
            file.write(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")+ " - "+ message+ "\n")

    def book_table(self, staff_id):

        print("\n========== BOOK TABLE ==========")
        print("Type 'back' to return.")

        table_id = input("Enter Table ID: ").strip()

        if table_id.lower() == "back":
            return

        if not table_id.isdigit() or len(table_id) != 4:

            self.save_error("Invalid table ID.")
            print("Table ID must contain exactly 4 digits.")
            return

        tables = self.load_tables()
        bookings = self.load_bookings()

        table = None

        for item in tables:

            if str(item.get("id")).strip() == table_id:
                table = item
                break

        if table is None:

            self.save_error("Table not found.")
            print("Table not found.")
            return

        if str(table.get("status")).strip().lower() == "booked":

            print("Table is already booked.")
            return

        customer_name = input("Enter Customer Name: ").strip()

        if customer_name.lower() == "back":
            return

        if not customer_name:

            self.save_error("Invalid customer name.")
            print("Customer name cannot be empty.")
            return

        customer_phone = input("Enter Customer Phone (10 digits): ").strip()

        if customer_phone.lower() == "back":
            return

        if not customer_phone.isdigit() or len(customer_phone) != 10:

            self.save_error("Invalid customer phone number.")
            print("Customer phone must contain exactly 10 digits.")
            return

        people = input("Enter Number of People: ").strip()

        if people.lower() == "back":
            return

        if not people.isdigit() or int(people) <= 0:

            self.save_error("Invalid number of people.")
            print("Number of people must be greater than 0.")
            return

        booking_id = str(8000000000 + len(bookings) + 1)

        while any(
            booking.get("id") == booking_id
            for booking in bookings):
            
            booking_id = str(int(booking_id) + 1)

        booking = {
            "id": booking_id,
            "table_id": table_id,
            "staff_id": staff_id,
            "customer_name": customer_name,
            "customer_phone": customer_phone,
            "people": int(people),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Active"}

        bookings.append(booking)

        table["status"] = "Booked"

        self.save_bookings(bookings)
        self.save_tables(tables)

        self.log("Table booked: " + booking_id)

        print("\nTable booked successfully.")
        print("Booking ID:", booking_id)
        print("Table ID:", table_id)
        print("Customer:", customer_name)


class BookingStatus:

    def __init__(
        self,
        booking_file=None,
        log_file=None,
        error_file=None
    ):
        self.booking_file = booking_file or os.path.join(BASE_DIR, "database", "bookings.json")
        self.log_file = log_file or os.path.join(BASE_DIR, "logs", "velmora.log")
        self.error_file = error_file or os.path.join(BASE_DIR, "errors", "errors.json")
        self.create_files()

    def create_files(self):

        for file_path in [
            self.booking_file,
            self.log_file,
            self.error_file]:
            
            folder = os.path.dirname(file_path)

            if folder and not os.path.exists(folder):
                os.makedirs(folder)

            if not os.path.exists(file_path):

                if file_path.endswith(".json"):
                    with open(file_path, "w") as file:
                        json.dump([], file, indent=4)

                else:
                    with open(file_path, "w") as file:
                        file.write("")

    def load_bookings(self):

        try:
            with open(self.booking_file, "r") as file:
                return json.load(file)

        except:
            return []

    def save_error(self, message):

        errors = []

        try:
            with open(self.error_file, "r") as file:
                errors = json.load(file)

        except:
            errors = []

        errors.append({
            "error": message,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

        with open(self.error_file, "w") as file:
            json.dump(errors, file, indent=4)

    def log(self, message):

        with open(self.log_file, "a") as file:
            file.write(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")+ " - "+ message+ "\n")

    def booking_status(self, staff_id=None):

        print("\n========== BOOKING STATUS ==========")

        bookings = self.load_bookings()

        if staff_id is not None:

            bookings = [
                booking for booking in bookings
                if booking.get("staff_id") == staff_id]

        if not bookings:

            print("No bookings found.")
            return

        for booking in bookings:

            print("\nBooking ID:", booking.get("id"))
            print("Table ID:", booking.get("table_id"))
            print("Customer Name:", booking.get("customer_name"))
            print("People:", booking.get("people"))
            print("Date:", booking.get("date"))
            print("Status:", booking.get("status"))

        self.log("Booking status viewed.")


class CancelBooking:

    def __init__(
        self,
        table_file=None,
        booking_file=None,
        log_file=None,
        error_file=None
    ):
        self.table_file = table_file or os.path.join(BASE_DIR, "database", "tables.json")
        self.booking_file = booking_file or os.path.join(BASE_DIR, "database", "bookings.json")
        self.log_file = log_file or os.path.join(BASE_DIR, "logs", "velmora.log")
        self.error_file = error_file or os.path.join(BASE_DIR, "errors", "errors.json")
        self.create_files()

    def create_files(self):

        for file_path in [
            self.table_file,
            self.booking_file,
            self.log_file,
            self.error_file
        ]:
            folder = os.path.dirname(file_path)

            if folder and not os.path.exists(folder):
                os.makedirs(folder)

            if not os.path.exists(file_path):

                if file_path.endswith(".json"):
                    with open(file_path, "w") as file:
                        json.dump([], file, indent=4)

                else:
                    with open(file_path, "w") as file:
                        file.write("")

    def normalize_tables(self, tables):
        if not isinstance(tables, list):
            return []

        normalized = []

        for table in tables:
            if isinstance(table, dict):
                normalized.append(table)
            elif isinstance(table, list):
                normalized.extend(self.normalize_tables(table))

        return normalized

    def load_tables(self):

        try:
            with open(self.table_file, "r") as file:
                return self.normalize_tables(json.load(file))

        except:
            return []

    def save_tables(self, tables):

        with open(self.table_file, "w") as file:
            json.dump(self.normalize_tables(tables), file, indent=4)

    def load_bookings(self):

        try:
            with open(self.booking_file, "r") as file:
                return json.load(file)

        except:
            return []

    def save_bookings(self, bookings):

        with open(self.booking_file, "w") as file:
            json.dump(bookings, file, indent=4)

    def save_error(self, message):

        errors = []

        try:
            with open(self.error_file, "r") as file:
                errors = json.load(file)

        except:
            errors = []

        errors.append({
            "error": message,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

        with open(self.error_file, "w") as file:
            json.dump(errors, file, indent=4)

    def log(self, message):

        with open(self.log_file, "a") as file:
            file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+ " - "+ message+ "\n")

    @staticmethod
    def normalize_id(value):
        return str(value).strip()

    @staticmethod
    def normalize_status(value):
        return str(value).strip().upper()

    def cancel_booking(self, staff_id=None):

        print("\n========== CANCEL BOOKING ==========")
        print("Type 'back' to return.")

        booking_id = input("Enter Booking ID: ").strip()

        if booking_id.lower() == "back":
            return

        if not booking_id.isdigit() or len(booking_id) != 10:

            self.save_error("Invalid booking ID.")
            print("Booking ID must contain exactly 10 digits.")
            return

        bookings = self.load_bookings()
        tables = self.load_tables()

        booking = None

        for item in bookings:

            if self.normalize_id(item.get("id")) == booking_id:
                booking = item
                break

        if booking is None:

            self.save_error("Booking not found.")
            print("Booking not found.")
            return

        if staff_id is not None and self.normalize_id(booking.get("staff_id")) != self.normalize_id(staff_id):

            self.save_error("Staff tried to cancel another staff booking.")
            print("You can only cancel your own booking.")
            return

        if self.normalize_status(booking.get("status")) == "CANCELLED":

            print("Booking is already cancelled.")
            return

        confirm = input("Cancel this booking? (yes/no): ").strip().lower()

        if confirm == "back" or confirm == "no":
            return

        if confirm != "yes":

            self.save_error("Invalid cancellation choice.")
            print("Please enter yes or no.")
            return

        booking["status"] = "Cancelled"

        table_id = booking.get("table_id")

        for table in tables:

            if self.normalize_id(table.get("id")) == self.normalize_id(table_id):
                table["status"] = "Available"
                break

        self.save_bookings(bookings)
        self.save_tables(tables)

        self.log("Booking cancelled: " + booking_id)

        print("\nBooking cancelled successfully.")
        print("Table is now available.")


class ViewTable:

    def __init__(
        self,
        file_path=None,
        log_file=None
    ):
        self.file_path = file_path or os.path.join(BASE_DIR, "database", "tables.json")
        self.log_file = log_file or os.path.join(BASE_DIR, "logs", "velmora.log")
        self.create_files()

    def create_files(self):

        folder = os.path.dirname(self.file_path)

        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        log_folder = os.path.dirname(self.log_file)

        if log_folder and not os.path.exists(log_folder):
            os.makedirs(log_folder)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as file:
                json.dump([], file, indent=4)

        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as file:
                file.write("")

    def write_log(self, message):

        with open(self.log_file, "a") as file:
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{time}] {message}\n")

    def normalize_tables(self, tables):
        if not isinstance(tables, list):
            return []

        normalized = []

        for table in tables:
            if isinstance(table, dict):
                normalized.append(table)
            elif isinstance(table, list):
                normalized.extend(self.normalize_tables(table))

        return normalized

    def load_tables(self):

        try:
            with open(self.file_path, "r") as file:
                tables = json.load(file)

            return self.normalize_tables(tables)

        except (json.JSONDecodeError, FileNotFoundError):
            self.write_log("Error while reading table data.")
            return []

    def view_tables(self):

        tables = self.load_tables()

        print()
        print("==================================================================================")
        print("                              VELMORA RESTAURANT")
        print("                                   TABLE LIST")
        print("==================================================================================")
        print()
        print("ID          TABLE NUMBER            CATEGORY            SEATS           STATUS")
        print("----------------------------------------------------------------------------------")

        if not tables:
            print("                       No tables available.")
            print("----------------------------------------------------------------------------------")
            self.write_log("View Table opened - no tables available.")
            return

        for table in tables:

            if not isinstance(table, dict):
                continue

            table_id = str(table.get("id", ""))
            table_number = str(table.get("table_number", ""))
            category = str(table.get("category", ""))
            seats = str(table.get("seats", ""))
            status = str(table.get("status", "")).upper()

            print(
                f"{table_id:<14}"
                f"{table_number:<21}"
                f"{category:<20}"
                f"{seats:<18}"
                f"{status}"
            )

        print("----------------------------------------------------------------------------------")
        print()

        self.write_log("All tables viewed successfully.")

    def display_tables(self):
        self.view_tables()

    def run(self):
        self.view_tables()
if __name__ == "__main__":
    view_table = ViewTable()
    view_table.run()
