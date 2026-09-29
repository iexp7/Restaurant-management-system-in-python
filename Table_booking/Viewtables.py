import json
import os
from datetime import datetime


class ViewTables:
    def __init__(self, file_path="data/tables.json",
                 log_file="logs/velmora.log",
                 error_file="errors/errors.json"):
        self.file_path = file_path
        self.log_file = log_file
        self.error_file = error_file
        self.create_files()
        self.create_tables()

    def create_files(self):
        for path in [self.file_path, self.log_file, self.error_file]:
            folder = os.path.dirname(path)

            if folder and not os.path.exists(folder):
                os.makedirs(folder)

            if not os.path.exists(path):
                with open(path, "w") as file:
                    json.dump([], file) if path.endswith(".json") else file.write("")

    def load_tables(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except:
            self.save_error("Unable to read tables.json.")
            return []

    def save_tables(self, tables):
        with open(self.file_path, "w") as file:
            json.dump(tables, file, indent=4)

    def create_tables(self):
        tables = self.load_tables()

        if tables:
            return

        for number in range(1, 11):
            tables.append({
                "id": str(6000000000 + number),
                "table_number": number,
                "status": "Available"
            })

        self.save_tables(tables)
        self.log("Default tables created.")

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

    def view_tables(self):
        tables = self.load_tables()

        print("\n========== VELMORA TABLES ==========")

        if not tables:
            print("No tables available.")
            return

        for table in tables:
            print("\nTable ID     :", table.get("id"))
            print("Table Number :", table.get("table_number"))
            print("Status       :", table.get("status"))
            print("-----------------------------------")

        self.log("Tables viewed.")