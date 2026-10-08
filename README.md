# Velmora Restaurant Management System

Velmora Restaurant Management System is a **Python-based restaurant management project** designed to manage users, menu items, orders, billing, inventory, and table bookings.

The project is built with a focus on **simple code, easy understanding, validation, JSON-based data storage, and a beginner-friendly structure**.

---

## Project Name

**Velmora Restaurant Management System**

---

## Project Objective

The main objective of Velmora is to provide a simple restaurant management system that can handle:

- User Authentication
- Admin Management
- Staff Management
- Menu Management
- Order Management
- Billing
- Inventory Management
- Table Booking
- Error Handling
- Activity Logging

---

## Technologies Used

- **Python**
- **JSON** — Data storage
- **OS** — File and folder handling
- **Datetime** — Date and time
- **Maskpass** — Hidden password input

### Allowed Python Modules

```text
json
os
datetime
maskpass
```

No unnecessary external libraries are used.

---

## User Roles

### Admin

Velmora has only **one Admin account**.

```
Username: bhup3ndr@
Password: 291769
```

The Admin can:

- Manage Staff
- Add Staff
- View Staff
- Remove Staff
- Manage Menu
- Manage Orders
- Book a table for a customer and create dine-in or takeaway orders
- Access administrative options

### Waitstaff

Multiple staff accounts can be created.

Staff can access limited restaurant operations such as:

- View Menu
- Create dine-in or takeaway orders
- View Order
- Update Order
- Cancel Order
- View Stock
- View Tables
- Book Table
- Cancel Booking
- Check Booking Status

Staff cannot manage other staff accounts.


## Menu

Velmora contains both **Asian and Western food items**.

Each food item supports:

- Full portion
- Half portion
- 10-digit Item ID
- Category
- Price

Restaurant table IDs use exactly 4 digits (for example, `0001`).

Example categories:

```
Asian
Western
```

---

## Billing

The billing system is designed to support:

- Customer name and phone number
- Dine-in booking/table details or takeaway order type
- Itemized bill with item ID, size, quantity, unit price, and line total
- Order Subtotal
- Discount
- **5% GST**
- Final Bill
- Cash Payment
- Card Payment
- Online Payment

Billing functionality is implemented together in `app/Billing/billing.py`.

---

## ID System

Important records use **10-digit IDs**.

Examples:

```****
text
Admin ID     → 1000000001
Menu Item ID → 2000000001
Order ID     → 3000000001
```****

Separate ID ranges make records easier to identify.

---

## Project(Files) Structure :)

```text
Velmora/
│
├── main.py
├── display.py
│
├── data/
│   ├── users.json
│   ├── menu.json
│   ├── orders.json
│   ├── inventory.json
│   ├── tables.json
│   └── bookings.json
│
├── errors/
│   └── errors.json
│
├── logs/
│   └── velmora.log
│
├── user_authentication/
│   ├── registration.py
│   ├── login.py
│   ├── admin.py
│   ├── waitstaff.py
│   └── user.py
│
├── menu_management/
│   ├── menu.py
│   ├── add_item.py
│   ├── view_item.py
│   ├── update_item.py
│   └── delete_item.py
│
├── order_management/
│   ├── order_management.py
│   ├── create_order.py
│   ├── view_order.py
│   ├
