import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Menu:
    def __init__(self, file_path=None, log_file=None, error_file=None):
        self.file_path = file_path or os.path.join(BASE_DIR, "database", "menu.json")
        self.log_file = log_file or os.path.join(BASE_DIR, "logs", "velmora.log")
        self.error_file = error_file or os.path.join(BASE_DIR, "errors", "errors.json")
        self.create_files()
        self.create_default_menu()

    def create_files(self):
        for path in [self.file_path, self.log_file, self.error_file]:
            folder = os.path.dirname(path)

            if folder and not os.path.exists(folder):
                os.makedirs(folder)

            if not os.path.exists(path):
                with open(path, "w") as file:
                    json.dump([], file) if path.endswith(".json") else file.write("")

    def load_items(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except:
            self.save_error("Unable to read menu.json.")
            return []

    def save_items(self, items):
        with open(self.file_path, "w") as file:
            json.dump(items, file, indent=4)

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

    def create_default_menu(self):
        items = self.load_items()

        if items:
            return

        items = [
            {
                "id": "1001",
                "name": "Chicken Biryani",
                "category": "Asian",
                "full": 220,
                "half": 130
            },
            {
                "id": "1002",
                "name": "Chicken Fried Rice",
                "category": "Asian",
                "full": 180,
                "half": 110
            },
            {
                "id": "1003",
                "name": "Veg Fried Rice",
                "category": "Asian",
                "full": 150,
                "half": 90
            },
            {
                "id": "1004",
                "name": "Hakka Noodles",
                "category": "Asian",
                "full": 160,
                "half": 95
            },
            {
                "id": "1005",
                "name": "Chilli Chicken",
                "category": "Asian",
                "full": 210,
                "half": 125
            },
            {
                "id": "1006",
                "name": "Chicken Manchurian",
                "category": "Asian",
                "full": 200,
                "half": 120
            },
            {
                "id": "1007",
                "name": "Paneer Tikka",
                "category": "Asian",
                "full": 190,
                "half": 115
            },
            {
                "id": "1008",
                "name": "Spring Rolls",
                "category": "Asian",
                "full": 140,
                "half": 85
            },
            {
                "id": "1009",
                "name": "Momos",
                "category": "Asian",
                "full": 130,
                "half": 80
            },
            {
                "id": "1010",
                "name": "Thai Noodles",
                "category": "Asian",
                "full": 180,
                "half": 110
            },
            {
                "id": "1011",
                "name": "Chicken Burger",
                "category": "Western",
                "full": 180,
                "half": 110
            },
            {
                "id": "1012",
                "name": "Veg Burger",
                "category": "Western",
                "full": 150,
                "half": 90
            },
            {
                "id": "1013",
                "name": "Chicken Pizza",
                "category": "Western",
                "full": 280,
                "half": 170
            },
            {
                "id": "1014",
                "name": "Margherita Pizza",
                "category": "Western",
                "full": 240,
                "half": 150
            },
            {
                "id": "1015",
                "name": "Pasta Alfredo",
                "category": "Western",
                "full": 220,
                "half": 135
            },
            {
                "id": "1016",
                "name": "Chicken Steak",
                "category": "Western",
                "full": 320,
                "half": 190
            },
            {
                "id": "1017",
                "name": "French Fries",
                "category": "Western",
                "full": 120,
                "half": 70
            },
            {
                "id": "1018",
                "name": "Garlic Bread",
                "category": "Western",
                "full": 130,
                "half": 80
            },
            {
                "id": "1019",
                "name": "Grilled Sandwich",
                "category": "Western",
                "full": 150,
                "half": 90
            },
            {
                "id": "1020",
                "name": "Chicken Wrap",
                "category": "Western",
                "full": 170,
                "half": 100
            },
    {
        "id": "2000000021",
        "name": "Coca Cola",
        "category": "Drinks",
        "price": 60
    },
    {
        "id": "2000000022",
        "name": "Pepsi",
        "category": "Drinks",
        "price": 60
    },
    {
        "id": "2000000023",
        "name": "Sprite",
        "category": "Drinks",
        "price": 60
    },
    {
        "id": "2000000024",
        "name": "Fanta",
        "category": "Drinks",
        "price": 60
    },
    {
        "id": "2000000025",
        "name": "Fresh Lime Soda",
        "category": "Drinks",
        "price": 80
    },
    {
        "id": "2000000026",
        "name": "Cold Coffee",
        "category": "Drinks",
        "price": 120
    },
    {
        "id": "2000000027",
        "name": "Mango Shake",
        "category": "Drinks",
        "price": 130
    },
    {
        "id": "2000000028",
        "name": "Strawberry Shake",
        "category": "Drinks",
        "price": 140
    },
    {
        "id": "2000000029",
        "name": "Iced Tea",
        "category": "Drinks",
        "price": 90
    },
    {
        "id": "2000000030",
        "name": "Mineral Water",
        "category": "Drinks",
        "price": 30
    }
    ]

        self.save_items(items)
        self.log("Default Velmora menu created.")

    def get_item(self, item_id):
        items = self.load_items()

        for item in items:
            if item.get("id") == item_id:
                return item

        self.save_error("Menu item not found: " + item_id)
        return None


class AddItem:
    def __init__(self, file_path=None, log_file=None, error_file=None):
        self.file_path = file_path or os.path.join(BASE_DIR, "database", "menu.json")
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

    def load_items(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except:
            self.save_error("Unable to read menu.json.")
            return []

    def save_items(self, items):
        with open(self.file_path, "w") as file:
            json.dump(items, file, indent=4)

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

    def add_item(self):
        items = self.load_items()

        print("\n===== ADD MENU ITEM =====")
        print("Type 'back' at any time to return.")

        name = input("Item name: ").strip()

        if name.lower() == "back":
            return

        if not name:
            self.save_error("Empty item name.")
            print("Item name cannot be empty.")
            return

        for item in items:
            if item.get("name", "").lower() == name.lower():
                self.save_error("Duplicate menu item: " + name)
                print("Item already exists.")
                return

        category = input("Category (Asian/Western/Drinks): ").strip()

        if category.lower() == "back":
            return

        if category.lower() not in ["asian", "western", "drinks"]:
            self.save_error("Invalid menu category.")
            print("Category must be Asian, Western or Drinks.")
            return

        if category.lower() == "drinks":

            try:
                price = float(input("Price: "))

                if price <= 0:
                    raise ValueError

            except:
                self.save_error("Invalid drink price entered.")
                print("Enter a valid price.")
                return

        else:

            try:
                full = float(input("Full price: "))

                if full <= 0:
                    raise ValueError

                half = float(input("Half price: "))

                if half <= 0 or half >= full:
                    raise ValueError

            except:
                self.save_error("Invalid menu price entered.")
                print("Enter valid prices. Half price must be less than Full price.")
                return

        if category.lower() == "drinks":
            item_id = str(2000000000 + len(items) + 1)

            while any(item.get("id") == item_id for item in items):
                item_id = str(int(item_id) + 1)
        else:
            food_ids = {
                int(item["id"])
                for item in items
                if str(item.get("category", "")).lower() != "drinks"
                and str(item.get("id", "")).isdigit()
                and len(str(item.get("id", ""))) == 4
            }
            next_id = max(food_ids, default=1000) + 1

            if next_id > 9999:
                self.save_error("No 4-digit food IDs are available.")
                print("No 4-digit food IDs are available.")
                return

            item_id = str(next_id)

        if category.lower() == "drinks":

            item = {
                "id": item_id,
                "name": name,
                "category": "Drinks",
                "price": price
            }

        else:

            item = {
                "id": item_id,
                "name": name,
                "category": category.title(),
                "full": full,
                "half": half
            }

        items.append(item)
        self.save_items(items)

        self.log("Menu item added: " + name)

        print("\nItem added successfully.")
        print("Item ID:", item_id)


class ViewItem:

    def __init__(
        self,
        file_path=None,
        log_file=None):

        self.file_path = file_path or os.path.join(BASE_DIR, "database", "menu.json")
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

    def load_items(self):

        try:
            with open(self.file_path, "r") as file:
                items = json.load(file)

            if not isinstance(items, list):
                self.write_log("Menu data must be a JSON list.")
                return []

            return items

        except (json.JSONDecodeError, OSError):
            self.write_log("Error while reading menu items.")
            return []

    def display_items(self):

        items = self.load_items()
        valid_items = []
        invalid_items = 0

        for item in items:
            if isinstance(item, dict):
                valid_items.append(item)
            else:
                invalid_items += 1

        if invalid_items:
            self.write_log(
                f"Skipped {invalid_items} invalid menu item record(s).")
            print("Invalid menu entries were skipped.")

        if not valid_items:
            print("\nNo menu items available.")
            self.write_log("View Item opened - no items available.")
            return

        categories = {}
        for item in valid_items:
            category = str(item.get("category", "Other")).strip().title()
            category = category or "Other"
            categories.setdefault(category, []).append(item)

        category_order = ["Asian", "Western", "Drinks"]
        category_order.extend(
            sorted(category for category in categories
                   if category not in category_order))

        for category in category_order:
            category_items = categories.get(category, [])
            if not category_items:
                continue
            print()
            print(f"============== {category.upper()} MENU ==============")

            if category == "Drinks":
                headers = ["ID", "DRINK", "PRICE"]
                rows = [
                    [
                        str(item.get("id", "")),
                        str(item.get("name", "Unknown")),
                        "Rs." + str(item.get("price", 0))
                    ]
                    for item in category_items
                ]
            else:
                headers = ["ID", "FOOD ITEM", "OPTION", "PRICE"]
                rows = []
                for item in category_items:
                    item_id = str(item.get("id", ""))
                    name = str(item.get("name", "Unknown"))
                    full_price = item.get("full_price", item.get("full", 0))
                    half_price = item.get("half_price", item.get("half", 0))
                    rows.extend([
                        [item_id, name, "Full", "Rs." + str(full_price)],
                        ["", "", "Half", "Rs." + str(half_price)]
                    ])

            widths = [
                max(len(header), *(len(row[index]) for row in rows))
                for index, header in enumerate(headers)
            ]
            border = "+" + "+".join(
                "-" * (width + 2) for width in widths
            ) + "+"

            print(border)
            print(
                "| "
                + " | ".join(
                    f"{header:<{width}}"
                    for header, width in zip(headers, widths)
                )
                + " |")
            print(border)

            for row in rows:
                print(
                    "| "
                    + " | ".join(
                        f"{value:<{width}}"
                        for value, width in zip(row, widths)
                    )
                    + " |")

            print(border)

        self.write_log("Menu items viewed successfully.")

    def view_items(self):
        self.display_items()

    def run(self):
        self.display_items()


class UpdateItem:
    def __init__(self, file_path=None, log_file=None, error_file=None):
        self.file_path = file_path or os.path.join(BASE_DIR, "database", "menu.json")
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

    def load_items(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except:
            self.save_error("Unable to read menu.json.")
            return []

    def save_items(self, items):
        with open(self.file_path, "w") as file:
            json.dump(items, file, indent=4)

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
            file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                       + " - " + message + "\n")

    def update_item(self):
        items = self.load_items()

        print("\n===== UPDATE MENU ITEM =====")
        print("Type 'back' to return.")

        item_id = input("Enter Item ID: ").strip()

        if item_id.lower() == "back":
            return

        if not item_id.isdigit() or len(item_id) not in (4, 10):
            self.save_error("Invalid menu item ID.")
            print("Food item IDs must contain 4 digits; drink IDs must contain 10 digits.")
            return

        item = None

        for data in items:
            if data.get("id") == item_id:
                item = data
                break

        if item is None:
            self.save_error("Menu item not found: " + item_id)
            print("Item not found.")
            return

        name = input("New name: ").strip()

        if name.lower() == "back":
            return

        if not name:
            self.save_error("Empty item name during update.")
            print("Name cannot be empty.")
            return

        category = input("Category (Asian/Western/Drink): ").strip()

        if category.lower() == "back":
            return

        if category.lower() not in ["asian", "western","Drinks"]:
            self.save_error("Invalid category during menu update.")
            print("Category must be Asian or Western.")
            return

        try:
            full = float(input("New Full price: "))
            half = float(input("New Half price: "))

            if full <= 0 or half <= 0 or half >= full:
                raise ValueError

        except:
            self.save_error("Invalid price during menu update.")
            print("Invalid price. Half price must be less than Full price.")
            return

        item["name"] = name
        item["category"] = category.title()
        item["full"] = full
        item["half"] = half

        self.save_items(items)
        self.log("Menu item updated: " + item_id)

        print("\nMenu item updated successfully.")


class DeleteItem:
    def __init__(self, file_path=None, log_file=None, error_file=None):
        self.file_path = file_path or os.path.join(BASE_DIR, "database", "menu.json")
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

    def load_items(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except:
            self.save_error("Unable to read menu.json.")
            return []

    def save_items(self, items):
        with open(self.file_path, "w") as file:
            json.dump(items, file, indent=4)

    def save_error(self, message):
        try:
            with open(self.error_file, "r") as file:
                errors = json.load(file)
        except:
            errors = []

        errors.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"message": message})

        with open(self.error_file, "w") as file:
            json.dump(errors, file, indent=4)

    def log(self, message):
        with open(self.log_file, "a") as file:
            file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+ " - " + message + "\n")

    def delete_item(self):
        items = self.load_items()

        print("\n===== DELETE MENU ITEM =====")
        print("Type 'back' to return.")

        item_id = input("Enter Item ID: ").strip()

        if item_id.lower() == "back":
            return

        if not item_id.isdigit() or len(item_id) not in (4, 10):
            self.save_error("Invalid menu item ID during delete.")
            print("Food item IDs must contain 4 digits; drink IDs must contain 10 digits.")
            return

        for item in items:
            if item.get("id") == item_id:
                print("\nItem:", item.get("name"))
                confirm = input("Delete this item? (yes/no): ").strip().lower()

                if confirm == "back" or confirm == "no":
                    print("Delete cancelled.")
                    return

                if confirm != "yes":
                    self.save_error("Invalid delete confirmation.")
                    print("Enter yes or no.")
                    return

                items.remove(item)
                self.save_items(items)

                self.log("Menu item deleted: " + item_id)
                print("Item deleted successfully.")
                return

        self.save_error("Menu item not found: " + item_id)
        print("Item not found.")
if __name__ == "__main__":
    view_item = ViewItem()
    view_item.run()
