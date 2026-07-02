"""
OnlineStoreDB_046 - Simple Desktop GUI
----------------------------------------
Requirements:
    pip install mysql-connector-python

Before running:
    1. Make sure MySQL server is running and online_store.sql has been imported:
         mysql -u root -p < online_store.sql
    2. Edit the DB_CONFIG dictionary below with your MySQL host/user/password.
       (You said you'll add a password later -> just fill DB_CONFIG["password"].)

To run:
    python store_gui.py

Login:
    Use one of the accounts already inserted by your SQL script, e.g.
        username: manager1     password: manager123
        username: cashier1     password: cashier123
        username: inventory1   password: inventory123
"""

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# ------------------------------------------------------------------
# 1) DATABASE CONNECTION SETTINGS -- EDIT THESE
# ------------------------------------------------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",          # <-- put your MySQL password here
    "database": "OnlineStoreDB_046",
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def run_query(query, params=None, fetch=False, commit=False):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(query, params or ())
        result = cur.fetchall() if fetch else None
        columns = [d[0] for d in cur.description] if fetch and cur.description else []
        if commit:
            conn.commit()
        return result, columns
    finally:
        cur.close()
        conn.close()


# ------------------------------------------------------------------
# 2) LOGIN WINDOW
# ------------------------------------------------------------------
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Online Store - Login")
        self.geometry("320x220")
        self.resizable(False, False)

        ttk.Label(self, text="Online Store Login", font=("Segoe UI", 14, "bold")).pack(pady=15)

        form = ttk.Frame(self)
        form.pack(pady=5)

        ttk.Label(form, text="Username:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.username_entry = ttk.Entry(form)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Password:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = ttk.Entry(form, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self, text="Login", command=self.attempt_login).pack(pady=15)
        self.bind("<Return>", lambda e: self.attempt_login())

    def attempt_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Missing info", "Please enter both username and password.")
            return

        try:
            rows, _ = run_query(
                "SELECT user_id, username, role FROM Users_046 "
                "WHERE username = %s AND password = %s",
                (username, password),
                fetch=True,
            )
        except Error as e:
            messagebox.showerror("Database error", str(e))
            return

        if rows:
            user_id, uname, role = rows[0]
            self.destroy()
            app = MainApp(uname, role)
            app.mainloop()
        else:
            messagebox.showerror("Login failed", "Invalid username or password.")


# ------------------------------------------------------------------
# 3) MAIN APPLICATION WINDOW
# ------------------------------------------------------------------
class MainApp(tk.Tk):
    def __init__(self, username, role):
        super().__init__()
        self.username = username
        self.role = role
        self.title(f"Online Store Manager - {username} ({role})")
        self.geometry("900x550")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.products_tab = ProductsTab(notebook)
        self.inventory_tab = InventoryTab(notebook)
        self.customers_tab = CustomersTab(notebook)
        self.orders_tab = OrdersTab(notebook)

        notebook.add(self.products_tab, text="Products")
        notebook.add(self.inventory_tab, text="Inventory")
        notebook.add(self.customers_tab, text="Customers")
        notebook.add(self.orders_tab, text="Orders")


# ------------------------------------------------------------------
# Helper base class for a "table + search + refresh" tab
# ------------------------------------------------------------------
class BaseTableTab(ttk.Frame):
    columns = []
    base_query = ""

    def __init__(self, parent):
        super().__init__(parent)
        self.build_toolbar()
        self.build_table()
        self.refresh()

    def build_toolbar(self):
        bar = ttk.Frame(self)
        bar.pack(fill="x", pady=5, padx=5)

        ttk.Label(bar, text="Search:").pack(side="left", padx=(0, 5))
        self.search_var = tk.StringVar()
        entry = ttk.Entry(bar, textvariable=self.search_var, width=30)
        entry.pack(side="left")
        entry.bind("<Return>", lambda e: self.refresh())

        ttk.Button(bar, text="Search", command=self.refresh).pack(side="left", padx=5)
        ttk.Button(bar, text="Refresh", command=lambda: (self.search_var.set(""), self.refresh())).pack(side="left")

    def build_table(self):
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        vsb.place(relx=1.0, rely=0, relheight=1.0, anchor="ne")

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            rows, _ = run_query(self.search_query(), self.search_params(), fetch=True)
        except Error as e:
            messagebox.showerror("Database error", str(e))
            return
        for row in rows:
            self.tree.insert("", "end", values=row)

    def search_query(self):
        return self.base_query

    def search_params(self):
        return None


# ------------------------------------------------------------------
# Products tab
# ------------------------------------------------------------------
class ProductsTab(BaseTableTab):
    columns = ["product_id", "product_name", "category_name", "selling_price",
               "member_discount", "stock_quantity", "status"]
    base_query = """
        SELECT p.product_id, p.product_name, c.category_name, p.selling_price,
               p.member_discount, i.stock_quantity, p.status
        FROM Products_046 p
        JOIN Categories_046 c ON p.category_id = c.category_id
        JOIN Inventory_046 i ON p.product_id = i.product_id
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.build_add_form()

    def search_query(self):
        term = self.search_var.get().strip()
        if term:
            return self.base_query + " WHERE p.product_name LIKE %s"
        return self.base_query

    def search_params(self):
        term = self.search_var.get().strip()
        return (f"%{term}%",) if term else None

    def build_add_form(self):
        frame = ttk.LabelFrame(self, text="Add New Product")
        frame.pack(fill="x", padx=5, pady=5)

        labels = ["Name", "Description", "Selling Price", "Purchase Price",
                  "Discount %", "Category ID", "Supplier ID", "Stock Qty"]
        self.add_entries = {}
        for i, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=i // 4, column=(i % 4) * 2, sticky="e", padx=3, pady=3)
            entry = ttk.Entry(frame, width=15)
            entry.grid(row=i // 4, column=(i % 4) * 2 + 1, padx=3, pady=3)
            self.add_entries[label] = entry

        ttk.Button(frame, text="Add Product", command=self.add_product).grid(
            row=2, column=0, columnspan=8, pady=8)

    def add_product(self):
        try:
            name = self.add_entries["Name"].get().strip()
            desc = self.add_entries["Description"].get().strip()
            sell = float(self.add_entries["Selling Price"].get())
            purch = float(self.add_entries["Purchase Price"].get())
            disc = float(self.add_entries["Discount %"].get() or 0)
            cat_id = int(self.add_entries["Category ID"].get())
            sup_id = int(self.add_entries["Supplier ID"].get())
            stock = int(self.add_entries["Stock Qty"].get() or 0)
        except ValueError:
            messagebox.showwarning("Invalid input", "Please check numeric fields.")
            return

        if not name:
            messagebox.showwarning("Missing info", "Product name is required.")
            return

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO Products_046
                   (product_name, description, selling_price, purchase_price,
                    status, member_discount, category_id, supplier_id)
                   VALUES (%s,%s,%s,%s,'Available',%s,%s,%s)""",
                (name, desc, sell, purch, disc, cat_id, sup_id),
            )
            new_id = cur.lastrowid
            cur.execute(
                """INSERT INTO Inventory_046 (stock_quantity, reorder_level, product_id)
                   VALUES (%s, 10, %s)""",
                (stock, new_id),
            )
            conn.commit()
            cur.close()
            conn.close()
        except Error as e:
            messagebox.showerror("Database error", str(e))
            return

        messagebox.showinfo("Success", f"Product '{name}' added.")
        for entry in self.add_entries.values():
            entry.delete(0, "end")
        self.refresh()


# ------------------------------------------------------------------
# Inventory tab (low-stock focus)
# ------------------------------------------------------------------
class InventoryTab(BaseTableTab):
    columns = ["product_id", "product_name", "stock_quantity", "reorder_level", "last_updated"]
    base_query = """
        SELECT i.product_id, p.product_name, i.stock_quantity, i.reorder_level, i.last_updated
        FROM Inventory_046 i
        JOIN Products_046 p ON i.product_id = p.product_id
    """

    def __init__(self, parent):
        super().__init__(parent)
        ttk.Button(self, text="Show Low Stock Only", command=self.show_low_stock).pack(pady=5)

    def search_query(self):
        term = self.search_var.get().strip()
        if term:
            return self.base_query + " WHERE p.product_name LIKE %s"
        return self.base_query

    def search_params(self):
        term = self.search_var.get().strip()
        return (f"%{term}%",) if term else None

    def show_low_stock(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            rows, _ = run_query(
                self.base_query + " WHERE i.stock_quantity < i.reorder_level", fetch=True
            )
        except Error as e:
            messagebox.showerror("Database error", str(e))
            return
        for row in rows:
            self.tree.insert("", "end", values=row)


# ------------------------------------------------------------------
# Customers tab
# ------------------------------------------------------------------
class CustomersTab(BaseTableTab):
    columns = ["customer_id", "name", "email", "phone", "membership_level", "total_points"]
    base_query = """
        SELECT customer_id, name, email, phone, membership_level, total_points
        FROM Customers_046
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.build_add_form()

    def search_query(self):
        term = self.search_var.get().strip()
        if term:
            return self.base_query + " WHERE name LIKE %s OR email LIKE %s"
        return self.base_query

    def search_params(self):
        term = self.search_var.get().strip()
        return (f"%{term}%", f"%{term}%") if term else None

    def build_add_form(self):
        frame = ttk.LabelFrame(self, text="Add New Customer")
        frame.pack(fill="x", padx=5, pady=5)

        labels = ["Name", "Email", "Phone", "Address"]
        self.add_entries = {}
        for i, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=0, column=i * 2, sticky="e", padx=3, pady=3)
            entry = ttk.Entry(frame, width=18)
            entry.grid(row=0, column=i * 2 + 1, padx=3, pady=3)
            self.add_entries[label] = entry

        ttk.Button(frame, text="Add Customer", command=self.add_customer).grid(
            row=1, column=0, columnspan=8, pady=8)

    def add_customer(self):
        name = self.add_entries["Name"].get().strip()
        email = self.add_entries["Email"].get().strip()
        phone = self.add_entries["Phone"].get().strip()
        address = self.add_entries["Address"].get().strip()

        if not name or not email:
            messagebox.showwarning("Missing info", "Name and Email are required.")
            return

        try:
            run_query(
                """INSERT INTO Customers_046 (name, email, phone, address)
                   VALUES (%s,%s,%s,%s)""",
                (name, email, phone, address),
                commit=True,
            )
        except Error as e:
            messagebox.showerror("Database error", str(e))
            return

        messagebox.showinfo("Success", f"Customer '{name}' added.")
        for entry in self.add_entries.values():
            entry.delete(0, "end")
        self.refresh()


# ------------------------------------------------------------------
# Orders tab
# ------------------------------------------------------------------
class OrdersTab(BaseTableTab):
    columns = ["order_id", "customer_name", "order_date", "status", "total_amount"]
    base_query = """
        SELECT o.order_id, c.name, o.order_date, o.status, o.total_amount
        FROM Orders_046 o
        JOIN Customers_046 c ON o.customer_id = c.customer_id
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.build_status_form()

    def search_query(self):
        term = self.search_var.get().strip()
        if term:
            return self.base_query + " WHERE c.name LIKE %s"
        return self.base_query + " ORDER BY o.order_date DESC"

    def search_params(self):
        term = self.search_var.get().strip()
        return (f"%{term}%",) if term else None

    def build_status_form(self):
        frame = ttk.LabelFrame(self, text="Update Order Status")
        frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame, text="Order ID:").grid(row=0, column=0, padx=3, pady=5)
        self.order_id_entry = ttk.Entry(frame, width=10)
        self.order_id_entry.grid(row=0, column=1, padx=3, pady=5)

        ttk.Label(frame, text="New Status:").grid(row=0, column=2, padx=3, pady=5)
        self.status_var = tk.StringVar(value="Completed")
        status_combo = ttk.Combobox(
            frame, textvariable=self.status_var,
            values=["Pending", "Processing", "Completed", "Cancelled"],
            width=12, state="readonly",
        )
        status_combo.grid(row=0, column=3, padx=3, pady=5)

        ttk.Button(frame, text="Update Status", command=self.update_status).grid(
            row=0, column=4, padx=10, pady=5)

    def update_status(self):
        order_id = self.order_id_entry.get().strip()
        if not order_id.isdigit():
            messagebox.showwarning("Invalid input", "Enter a valid numeric Order ID.")
            return

        try:
            run_query(
                "UPDATE Orders_046 SET status = %s WHERE order_id = %s",
                (self.status_var.get(), int(order_id)),
                commit=True,
            )
        except Error as e:
            messagebox.showerror("Database error", str(e))
            return

        messagebox.showinfo(
            "Success",
            f"Order {order_id} status set to {self.status_var.get()}.\n"
            "(Note: if new status is 'Completed', the trg_member_points_046 "
            "trigger will auto-award loyalty points.)",
        )
        self.refresh()


# ------------------------------------------------------------------
if __name__ == "__main__":
    login = LoginWindow()
    login.mainloop()