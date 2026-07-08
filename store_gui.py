"""
OnlineStoreDB_046 - Simple Desktop GUI
----------------------------------------
Requirements:
    pip install mysql-connector-python

Before running:
    1. Make sure MySQL server is running and online_store.sql has been imported:
         mysql -u root -p < online_store.sql
    2. Edit the DB_CONFIG dictionary below with your MySQL host/user/password_046.

To run:
    python store_gui.py

Login:
    Use one of the accounts already inserted by your SQL script, e.g.
        username_046: manager1     password_046: manager123
        username_046: cashier1     password_046: cashier123
        username_046: inventory1   password_046: inventory123
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
    "password": "20Arslan03.",          # <-- put your MySQL password here
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
        username_046 = self.username_entry.get().strip()
        password_046 = self.password_entry.get().strip()

        if not username_046 or not password_046:
            messagebox.showwarning("Missing info", "Please enter both username_046 and password_046.")
            return

        try:
            rows, _ = run_query(
                "SELECT user_id_046, username_046, role_046 FROM Users_046 "
                "WHERE username_046 = %s AND password_046 = %s",
                (username_046, password_046),
                fetch=True,
            )
        except Error as e:
            messagebox.showerror("Database error", str(e))
            return

        if rows:
            user_id_046, uname, role_046 = rows[0]
            self.destroy()
            app = MainApp(uname, role_046)
            app.mainloop()
        else:
            messagebox.showerror("Login failed", "Invalid username_046 or password_046.")


# ------------------------------------------------------------------
# 3) MAIN APPLICATION WINDOW
# ------------------------------------------------------------------
class MainApp(tk.Tk):
    def __init__(self, username_046, role_046):
        super().__init__()
        self.username_046 = username_046
        self.role_046 = role_046
        self.title(f"Online Store Manager - {username_046} ({role_046})")
        self.geometry("900x550")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.products_tab = ProductsTab(notebook)
        self.inventory_tab = InventoryTab(notebook)
        self.customers_tab = CustomersTab(notebook)
        self.orders_tab = OrdersTab(notebook)
        self.place_order_tab = PlaceOrderTab(notebook)
        self.views_tab = ViewsTab(notebook)
        self.triggers_tab = TriggersTab(notebook)
        self.db_info_tab = DatabaseInfoTab(notebook)

        notebook.add(self.products_tab, text="Products")
        notebook.add(self.inventory_tab, text="Inventory")
        notebook.add(self.customers_tab, text="Customers")
        notebook.add(self.orders_tab, text="Orders")
        notebook.add(self.place_order_tab, text="Place Order")
        notebook.add(self.views_tab, text="Views")
        notebook.add(self.triggers_tab, text="Triggers")
        notebook.add(self.db_info_tab, text="Database Info")


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
    columns = ["product_id_046", "product_name_046", "category_name_046", "selling_price_046",
               "member_discount_046", "stock_quantity_046", "status_046"]
    base_query = """
        SELECT p.product_id_046, p.product_name_046, c.category_name_046, p.selling_price_046,
               p.member_discount_046, i.stock_quantity_046, p.status_046
        FROM Products_046 p
        JOIN Categories_046 c ON p.category_id_046 = c.category_id_046
        JOIN Inventory_046 i ON p.product_id_046 = i.product_id_046
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.build_add_form()
        self.build_edit_delete_form()
        self.tree.bind("<<TreeviewSelect>>", self.on_row_selected)

    def search_query(self):
        term = self.search_var.get().strip()
        if term:
            return self.base_query + " WHERE p.product_name_046 LIKE %s"
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

    def build_edit_delete_form(self):
        frame = ttk.LabelFrame(self, text="Update / Delete Selected Product (click a row above first)")
        frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame, text="Product ID:").grid(row=0, column=0, sticky="e", padx=3, pady=3)
        self.edit_id_entry = ttk.Entry(frame, width=8, state="readonly")
        self.edit_id_entry.grid(row=0, column=1, padx=3, pady=3)

        ttk.Label(frame, text="New Price:").grid(row=0, column=2, sticky="e", padx=3, pady=3)
        self.edit_price_entry = ttk.Entry(frame, width=12)
        self.edit_price_entry.grid(row=0, column=3, padx=3, pady=3)

        ttk.Label(frame, text="New Discount %:").grid(row=0, column=4, sticky="e", padx=3, pady=3)
        self.edit_discount_entry = ttk.Entry(frame, width=10)
        self.edit_discount_entry.grid(row=0, column=5, padx=3, pady=3)

        ttk.Label(frame, text="New Status:").grid(row=0, column=6, sticky="e", padx=3, pady=3)
        self.edit_status_var = tk.StringVar()
        ttk.Combobox(frame, textvariable=self.edit_status_var, width=11, state="readonly",
                     values=["Available", "Unavailable"]).grid(row=0, column=7, padx=3, pady=3)

        ttk.Button(frame, text="Update Product", command=self.update_product).grid(
            row=1, column=0, columnspan=4, pady=8)
        ttk.Button(frame, text="Delete Product", command=self.delete_product).grid(
            row=1, column=4, columnspan=4, pady=8)

    def on_row_selected(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0], "values")
        # values = [product_id_046, product_name_046, category_name_046, selling_price_046, member_discount_046, stock_quantity_046, status_046]
        self.edit_id_entry.config(state="normal")
        self.edit_id_entry.delete(0, "end")
        self.edit_id_entry.insert(0, values[0])
        self.edit_id_entry.config(state="readonly")

        self.edit_price_entry.delete(0, "end")
        self.edit_price_entry.insert(0, values[3])

        self.edit_discount_entry.delete(0, "end")
        self.edit_discount_entry.insert(0, values[4])

        self.edit_status_var.set(values[6])

    def update_product(self):
        pid = self.edit_id_entry.get().strip()
        if not pid:
            messagebox.showwarning("No selection", "Click a product row in the table first.")
            return
        try:
            price = float(self.edit_price_entry.get())
            discount = float(self.edit_discount_entry.get() or 0)
        except ValueError:
            messagebox.showwarning("Invalid input", "Price and discount must be numbers.")
            return
        status_046 = self.edit_status_var.get() or "Available"

        try:
            run_query(
                "UPDATE Products_046 SET selling_price_046 = %s, member_discount_046 = %s, status_046 = %s "
                "WHERE product_id_046 = %s",
                (price, discount, status_046, pid),
                commit=True,
            )
        except Error as e:
            messagebox.showerror("Database error", str(e))
            return

        messagebox.showinfo("Success", f"Product {pid} updated.")
        self.refresh()

    def delete_product(self):
        pid = self.edit_id_entry.get().strip()
        if not pid:
            messagebox.showwarning("No selection", "Click a product row in the table first.")
            return
        if not messagebox.askyesno("Confirm delete", f"Delete product ID {pid}? This cannot be undone."):
            return
        try:
            # Remove dependent Inventory row first to satisfy the foreign key.
            run_query("DELETE FROM Inventory_046 WHERE product_id_046 = %s", (pid,), commit=True)
            run_query("DELETE FROM Products_046 WHERE product_id_046 = %s", (pid,), commit=True)
        except Error as e:
            messagebox.showerror(
                "Database error",
                str(e) + "\n\nThis product may still be referenced by existing orders "
                         "(Order_Item_046) and cannot be deleted."
            )
            return

        messagebox.showinfo("Success", f"Product {pid} deleted.")
        self.refresh()

    def add_product(self):
        try:
            name_046 = self.add_entries["Name"].get().strip()
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

        if not name_046:
            messagebox.showwarning("Missing info", "Product name_046 is required.")
            return

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO Products_046
                   (product_name_046, description_046, selling_price_046, purchase_price_046,
                    status_046, member_discount_046, category_id_046, supplier_id_046)
                   VALUES (%s,%s,%s,%s,'Available',%s,%s,%s)""",
                (name_046, desc, sell, purch, disc, cat_id, sup_id),
            )
            new_id = cur.lastrowid
            cur.execute(
                """INSERT INTO Inventory_046 (stock_quantity_046, reorder_level_046, product_id_046)
                   VALUES (%s, 10, %s)""",
                (stock, new_id),
            )
            conn.commit()
            cur.close()
            conn.close()
        except Error as e:
            messagebox.showerror("Database error", str(e))
            return

        messagebox.showinfo("Success", f"Product '{name_046}' added.")
        for entry in self.add_entries.values():
            entry.delete(0, "end")
        self.refresh()


# ------------------------------------------------------------------
# Inventory tab (low-stock focus)
# ------------------------------------------------------------------
class InventoryTab(BaseTableTab):
    columns = ["product_id_046", "product_name_046", "stock_quantity_046", "reorder_level_046", "last_updated_046"]
    base_query = """
        SELECT i.product_id_046, p.product_name_046, i.stock_quantity_046, i.reorder_level_046, i.last_updated_046
        FROM Inventory_046 i
        JOIN Products_046 p ON i.product_id_046 = p.product_id_046
    """

    def __init__(self, parent):
        super().__init__(parent)
        ttk.Button(self, text="Show Low Stock Only", command=self.show_low_stock).pack(pady=5)
        self.build_update_qty_form()
        self.tree.bind("<<TreeviewSelect>>", self.on_row_selected)

    def search_query(self):
        term = self.search_var.get().strip()
        if term:
            return self.base_query + " WHERE p.product_name_046 LIKE %s"
        return self.base_query

    def search_params(self):
        term = self.search_var.get().strip()
        return (f"%{term}%",) if term else None

    def show_low_stock(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            rows, _ = run_query(
                self.base_query + " WHERE i.stock_quantity_046 < i.reorder_level_046", fetch=True
            )
        except Error as e:
            messagebox.showerror("Database error", str(e))
            return
        for row in rows:
            self.tree.insert("", "end", values=row)

    # ---- update stock quantity_046 ----
    def build_update_qty_form(self):
        frame = ttk.LabelFrame(self, text="Update Stock Quantity (click a row above first)")
        frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame, text="Product ID:").grid(row=0, column=0, sticky="e", padx=3, pady=3)
        self.qty_product_id_entry = ttk.Entry(frame, width=8, state="readonly")
        self.qty_product_id_entry.grid(row=0, column=1, padx=3, pady=3)

        ttk.Label(frame, text="New Stock Quantity:").grid(row=0, column=2, sticky="e", padx=3, pady=3)
        self.new_qty_entry = ttk.Entry(frame, width=10)
        self.new_qty_entry.grid(row=0, column=3, padx=3, pady=3)

        ttk.Label(frame, text="New Reorder Level:").grid(row=0, column=4, sticky="e", padx=3, pady=3)
        self.new_reorder_entry = ttk.Entry(frame, width=10)
        self.new_reorder_entry.grid(row=0, column=5, padx=3, pady=3)

        ttk.Button(frame, text="Update Quantity", command=self.update_quantity).grid(
            row=0, column=6, padx=10, pady=3)

    def on_row_selected(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0], "values")
        # values = [product_id_046, product_name_046, stock_quantity_046, reorder_level_046, last_updated_046]
        self.qty_product_id_entry.config(state="normal")
        self.qty_product_id_entry.delete(0, "end")
        self.qty_product_id_entry.insert(0, values[0])
        self.qty_product_id_entry.config(state="readonly")

        self.new_qty_entry.delete(0, "end")
        self.new_qty_entry.insert(0, values[2])

        self.new_reorder_entry.delete(0, "end")
        self.new_reorder_entry.insert(0, values[3])

    def update_quantity(self):
        pid = self.qty_product_id_entry.get().strip()
        if not pid:
            messagebox.showwarning("No selection", "Click an inventory row in the table first.")
            return
        try:
            new_qty = int(self.new_qty_entry.get())
            new_reorder = int(self.new_reorder_entry.get())
            if new_qty < 0 or new_reorder < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid input", "Quantity and reorder level must be non-negative whole numbers.")
            return

        try:
            run_query(
                "UPDATE Inventory_046 SET stock_quantity_046 = %s, reorder_level_046 = %s WHERE product_id_046 = %s",
                (new_qty, new_reorder, pid),
                commit=True,
            )
        except Error as e:
            messagebox.showerror("Database error", str(e))
            return

        messagebox.showinfo("Success", f"Inventory for product {pid} updated to {new_qty} unit(s).")
        self.refresh()


# ------------------------------------------------------------------
# Customers tab
# ------------------------------------------------------------------
class CustomersTab(BaseTableTab):
    columns = ["customer_id_046", "name_046", "email_046", "phone_046", "membership_level_046", "total_points_046"]
    base_query = """
        SELECT customer_id_046, name_046, email_046, phone_046, membership_level_046, total_points_046
        FROM Customers_046
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.build_add_form()
        self.build_edit_delete_form()
        self.tree.bind("<<TreeviewSelect>>", self.on_row_selected)

    def search_query(self):
        term = self.search_var.get().strip()
        if term:
            return self.base_query + " WHERE name_046 LIKE %s OR email_046 LIKE %s"
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

    def build_edit_delete_form(self):
        frame = ttk.LabelFrame(self, text="Update / Delete Selected Customer (click a row above first)")
        frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame, text="Customer ID:").grid(row=0, column=0, sticky="e", padx=3, pady=3)
        self.edit_id_entry = ttk.Entry(frame, width=8, state="readonly")
        self.edit_id_entry.grid(row=0, column=1, padx=3, pady=3)

        ttk.Label(frame, text="New Phone:").grid(row=0, column=2, sticky="e", padx=3, pady=3)
        self.edit_phone_entry = ttk.Entry(frame, width=14)
        self.edit_phone_entry.grid(row=0, column=3, padx=3, pady=3)

        ttk.Label(frame, text="New Membership:").grid(row=0, column=4, sticky="e", padx=3, pady=3)
        self.edit_membership_var = tk.StringVar()
        ttk.Combobox(frame, textvariable=self.edit_membership_var, width=10, state="readonly",
                     values=["Regular", "Silver", "Gold", "VIP"]).grid(row=0, column=5, padx=3, pady=3)

        ttk.Button(frame, text="Update Customer", command=self.update_customer).grid(
            row=1, column=0, columnspan=3, pady=8)
        ttk.Button(frame, text="Delete Customer", command=self.delete_customer).grid(
            row=1, column=3, columnspan=3, pady=8)

    def on_row_selected(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0], "values")
        # values = [customer_id_046, name_046, email_046, phone_046, membership_level_046, total_points_046]
        self.edit_id_entry.config(state="normal")
        self.edit_id_entry.delete(0, "end")
        self.edit_id_entry.insert(0, values[0])
        self.edit_id_entry.config(state="readonly")

        self.edit_phone_entry.delete(0, "end")
        self.edit_phone_entry.insert(0, values[3])

        self.edit_membership_var.set(values[4])

    def update_customer(self):
        cid = self.edit_id_entry.get().strip()
        if not cid:
            messagebox.showwarning("No selection", "Click a customer row in the table first.")
            return
        phone_046 = self.edit_phone_entry.get().strip()
        membership = self.edit_membership_var.get() or "Regular"

        try:
            run_query(
                "UPDATE Customers_046 SET phone_046 = %s, membership_level_046 = %s WHERE customer_id_046 = %s",
                (phone_046, membership, cid),
                commit=True,
            )
        except Error as e:
            messagebox.showerror("Database error", str(e))
            return

        messagebox.showinfo("Success", f"Customer {cid} updated.")
        self.refresh()

    def delete_customer(self):
        cid = self.edit_id_entry.get().strip()
        if not cid:
            messagebox.showwarning("No selection", "Click a customer row in the table first.")
            return
        if not messagebox.askyesno("Confirm delete", f"Delete customer ID {cid}? This cannot be undone."):
            return
        try:
            run_query("DELETE FROM Customers_046 WHERE customer_id_046 = %s", (cid,), commit=True)
        except Error as e:
            messagebox.showerror(
                "Database error",
                str(e) + "\n\nThis customer may still have existing orders and cannot be deleted."
            )
            return

        messagebox.showinfo("Success", f"Customer {cid} deleted.")
        self.refresh()

    def add_customer(self):
        name_046 = self.add_entries["Name"].get().strip()
        email_046 = self.add_entries["Email"].get().strip()
        phone_046 = self.add_entries["Phone"].get().strip()
        address_046 = self.add_entries["Address"].get().strip()

        if not name_046 or not email_046:
            messagebox.showwarning("Missing info", "Name and Email are required.")
            return

        try:
            run_query(
                """INSERT INTO Customers_046 (name_046, email_046, phone_046, address_046)
                   VALUES (%s,%s,%s,%s)""",
                (name_046, email_046, phone_046, address_046),
                commit=True,
            )
        except Error as e:
            messagebox.showerror("Database error", str(e))
            return

        messagebox.showinfo("Success", f"Customer '{name_046}' added.")
        for entry in self.add_entries.values():
            entry.delete(0, "end")
        self.refresh()


# ------------------------------------------------------------------
# Place Order tab (customer checkout - decreases stock via trigger)
# ------------------------------------------------------------------
class PlaceOrderTab(ttk.Frame):
    """
    Lets a customer 'buy' products. Builds a cart, then on submit:
      1. Creates one row in Orders_046
      2. Creates one row per cart item in Order_Item_046
         -> this fires trg_low_stock_warning_046, which automatically
            deducts stock_quantity_046 from Inventory_046 and logs a
            low-stock warning if it drops below reorder_level_046.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.cart = []  # list of dicts: {product_id_046, name_046, price, qty}
        self.build_customer_picker()
        self.build_product_picker()
        self.build_cart_view()

    # ---- customer selection ----
    def build_customer_picker(self):
        frame = ttk.LabelFrame(self, text="1. Select Customer")
        frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame, text="Customer:").pack(side="left", padx=5, pady=5)
        self.customer_var = tk.StringVar()
        self.customer_combo = ttk.Combobox(frame, textvariable=self.customer_var,
                                            width=40, state="readonly")
        self.customer_combo.pack(side="left", padx=5, pady=5)
        ttk.Button(frame, text="Refresh Customers", command=self.load_customers).pack(side="left", padx=5)
        self.load_customers()

    def load_customers(self):
        try:
            rows, _ = run_query(
                "SELECT customer_id_046, name_046, email_046 FROM Customers_046 ORDER BY name_046", fetch=True
            )
        except Error as e:
            messagebox.showerror("Database error", str(e))
            return
        self.customer_map = {f"{cid} - {name_046} ({email_046})": cid for cid, name_046, email_046 in rows}
        self.customer_combo["values"] = list(self.customer_map.keys())

    # ---- product / add-to-cart ----
    def build_product_picker(self):
        frame = ttk.LabelFrame(self, text="2. Add Product to Cart")
        frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame, text="Product:").pack(side="left", padx=5, pady=5)
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(frame, textvariable=self.product_var,
                                           width=45, state="readonly")
        self.product_combo.pack(side="left", padx=5, pady=5)
        ttk.Button(frame, text="Refresh Products", command=self.load_products).pack(side="left", padx=5)

        ttk.Label(frame, text="Qty:").pack(side="left", padx=(15, 5), pady=5)
        self.qty_entry = ttk.Entry(frame, width=6)
        self.qty_entry.insert(0, "1")
        self.qty_entry.pack(side="left", padx=5, pady=5)

        ttk.Button(frame, text="Add to Cart", command=self.add_to_cart).pack(side="left", padx=10)
        self.load_products()

    def load_products(self):
        try:
            rows, _ = run_query(
                """SELECT p.product_id_046, p.product_name_046, p.selling_price_046, i.stock_quantity_046
                   FROM Products_046 p
                   JOIN Inventory_046 i ON p.product_id_046 = i.product_id_046
                   WHERE p.status_046 = 'Available' AND i.stock_quantity_046 > 0
                   ORDER BY p.product_name_046""",
                fetch=True,
            )
        except Error as e:
            messagebox.showerror("Database error", str(e))
            return
        self.product_map = {}
        display = []
        for pid, name_046, price, stock in rows:
            label = f"{pid} - {name_046} (${price}, stock: {stock})"
            self.product_map[label] = {"product_id_046": pid, "name_046": name_046,
                                        "price": float(price), "stock": stock}
            display.append(label)
        self.product_combo["values"] = display

    def add_to_cart(self):
        label = self.product_var.get()
        if not label or label not in self.product_map:
            messagebox.showwarning("Missing info", "Please select a product.")
            return
        try:
            qty = int(self.qty_entry.get())
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid input", "Quantity must be a positive whole number.")
            return

        info = self.product_map[label]
        if qty > info["stock"]:
            messagebox.showwarning(
                "Not enough stock",
                f"Only {info['stock']} unit(s) of '{info['name_046']}' available."
            )
            return

        self.cart.append({
            "product_id_046": info["product_id_046"],
            "name_046": info["name_046"],
            "price": info["price"],
            "qty": qty,
        })
        self.refresh_cart_view()

    # ---- cart view + checkout ----
    def build_cart_view(self):
        frame = ttk.LabelFrame(self, text="3. Cart / Checkout")
        frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.cart_tree = ttk.Treeview(
            frame, columns=["product_id_046", "name_046", "price", "qty", "subtotal"], show="headings", height=8
        )
        for col in ["product_id_046", "name_046", "price", "qty", "subtotal"]:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=120, anchor="w")
        self.cart_tree.pack(fill="both", expand=True, padx=5, pady=5)

        bottom = ttk.Frame(frame)
        bottom.pack(fill="x", padx=5, pady=5)

        self.total_label = ttk.Label(bottom, text="Total: $0.00", font=("Segoe UI", 11, "bold"))
        self.total_label.pack(side="left", padx=5)

        ttk.Button(bottom, text="Remove Selected", command=self.remove_selected).pack(side="left", padx=5)
        ttk.Button(bottom, text="Clear Cart", command=self.clear_cart).pack(side="left", padx=5)
        ttk.Button(bottom, text="Submit Order", command=self.submit_order).pack(side="right", padx=5)

    def refresh_cart_view(self):
        for row in self.cart_tree.get_children():
            self.cart_tree.delete(row)
        total = 0.0
        for item in self.cart:
            subtotal = item["price"] * item["qty"]
            total += subtotal
            self.cart_tree.insert("", "end", values=(
                item["product_id_046"], item["name_046"], f"{item['price']:.2f}",
                item["qty"], f"{subtotal:.2f}"
            ))
        self.total_label.config(text=f"Total: ${total:.2f}")

    def remove_selected(self):
        sel = self.cart_tree.selection()
        if not sel:
            return
        index = self.cart_tree.index(sel[0])
        del self.cart[index]
        self.refresh_cart_view()

    def clear_cart(self):
        self.cart = []
        self.refresh_cart_view()

    def submit_order(self):
        label = self.customer_var.get()
        if not label or label not in self.customer_map:
            messagebox.showwarning("Missing info", "Please select a customer.")
            return
        if not self.cart:
            messagebox.showwarning("Empty cart", "Add at least one product to the cart.")
            return

        customer_id_046 = self.customer_map[label]
        total_amount_046 = sum(item["price"] * item["qty"] for item in self.cart)

        try:
            conn = get_connection()
            cur = conn.cursor()

            # 1) Create the order
            cur.execute(
                "INSERT INTO Orders_046 (status_046, total_amount_046, customer_id_046) "
                "VALUES ('Pending', %s, %s)",
                (total_amount_046, customer_id_046),
            )
            order_id_046 = cur.lastrowid

            # 2) Insert each cart item -> fires trg_low_stock_warning_046,
            #    which deducts stock automatically.
            for item in self.cart:
                cur.execute(
                    "INSERT INTO Order_Item_046 (quantity_046, unit_price_046, order_id_046, product_id_046) "
                    "VALUES (%s, %s, %s, %s)",
                    (item["qty"], item["price"], order_id_046, item["product_id_046"]),
                )

            conn.commit()
            cur.close()
            conn.close()
        except Error as e:
            messagebox.showerror("Database error", str(e))
            return

        messagebox.showinfo(
            "Order placed",
            f"Order #{order_id_046} created for ${total_amount_046:.2f}.\n"
            "Stock has been automatically deducted.\n"
            "If any product fell below its reorder level, check the "
            "Inventory tab's low-stock warnings."
        )
        self.clear_cart()
        self.load_products()  # refresh stock numbers shown in the dropdown


# ------------------------------------------------------------------
# Orders tab
# ------------------------------------------------------------------
class OrdersTab(BaseTableTab):
    columns = ["order_id_046", "customer_name", "order_date_046", "status_046", "total_amount_046"]
    base_query = """
        SELECT o.order_id_046, c.name_046, o.order_date_046, o.status_046, o.total_amount_046
        FROM Orders_046 o
        JOIN Customers_046 c ON o.customer_id_046 = c.customer_id_046
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.build_status_form()

    def search_query(self):
        term = self.search_var.get().strip()
        if term:
            return self.base_query + " WHERE c.name_046 LIKE %s"
        return self.base_query + " ORDER BY o.order_date_046 DESC"

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
        order_id_046 = self.order_id_entry.get().strip()
        if not order_id_046.isdigit():
            messagebox.showwarning("Invalid input", "Enter a valid numeric Order ID.")
            return

        try:
            run_query(
                "UPDATE Orders_046 SET status_046 = %s WHERE order_id_046 = %s",
                (self.status_var.get(), int(order_id_046)),
                commit=True,
            )
        except Error as e:
            messagebox.showerror("Database error", str(e))
            return

        messagebox.showinfo(
            "Success",
            f"Order {order_id_046} status_046 set to {self.status_var.get()}.\n"
            "(Note: if new status_046 is 'Completed', the trg_member_points_046 "
            "trigger will auto-award loyalty points.)",
        )
        self.refresh()


# ------------------------------------------------------------------
# Views tab - lets the user pick one of the SQL views and see its output
# ------------------------------------------------------------------
class ViewsTab(ttk.Frame):
    VIEWS = {
        "Cashier_Product_View_046": "SELECT * FROM Cashier_Product_View_046",
        "Management_Product_Sales_View_046": "SELECT * FROM Management_Product_Sales_View_046",
        "Member_Discount_Product_View_046": "SELECT * FROM Member_Discount_Product_View_046",
    }

    def __init__(self, parent):
        super().__init__(parent)
        self.build_toolbar()
        self.build_table()
        self.load_view(next(iter(self.VIEWS)))

    def build_toolbar(self):
        bar = ttk.Frame(self)
        bar.pack(fill="x", pady=5, padx=5)

        ttk.Label(bar, text="Select View:").pack(side="left", padx=(0, 5))
        self.view_var = tk.StringVar(value=next(iter(self.VIEWS)))
        combo = ttk.Combobox(
            bar, textvariable=self.view_var, values=list(self.VIEWS.keys()),
            width=40, state="readonly",
        )
        combo.pack(side="left", padx=5)
        ttk.Button(bar, text="Load View", command=lambda: self.load_view(self.view_var.get())).pack(
            side="left", padx=5)

    def build_table(self):
        self.tree = ttk.Treeview(self, show="headings")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        vsb.place(relx=1.0, rely=0, relheight=1.0, anchor="ne")

    def load_view(self, view_name):
        query = self.VIEWS.get(view_name)
        if not query:
            return
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            rows, columns = run_query(query, fetch=True)
        except Error as e:
            messagebox.showerror("Database error", str(e))
            return

        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="w")
        for row in rows:
            self.tree.insert("", "end", values=row)


# ------------------------------------------------------------------
# Triggers tab - lists the triggers defined on the database and their body
# ------------------------------------------------------------------
class TriggersTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Button(self, text="Refresh Triggers", command=self.refresh).pack(pady=5)
        self.build_table()
        self.build_detail_box()
        self.refresh()

    def build_table(self):
        self.columns = ["TRIGGER_NAME", "EVENT_MANIPULATION", "EVENT_OBJECT_TABLE", "ACTION_TIMING"]
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings", height=6)
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=160, anchor="w")
        self.tree.pack(fill="x", padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_selected)

    def build_detail_box(self):
        ttk.Label(self, text="Trigger Body:").pack(anchor="w", padx=5)
        self.detail_text = tk.Text(self, height=15, wrap="none")
        self.detail_text.pack(fill="both", expand=True, padx=5, pady=5)

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            rows, _ = run_query(
                """SELECT TRIGGER_NAME, EVENT_MANIPULATION, EVENT_OBJECT_TABLE, ACTION_TIMING
                   FROM information_schema.TRIGGERS
                   WHERE TRIGGER_SCHEMA = %s""",
                (DB_CONFIG["database"],),
                fetch=True,
            )
        except Error as e:
            messagebox.showerror("Database error", str(e))
            return
        for row in rows:
            self.tree.insert("", "end", values=row)

    def on_row_selected(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        trigger_name = self.tree.item(sel[0], "values")[0]
        try:
            rows, _ = run_query(
                """SELECT ACTION_STATEMENT FROM information_schema.TRIGGERS
                   WHERE TRIGGER_SCHEMA = %s AND TRIGGER_NAME = %s""",
                (DB_CONFIG["database"], trigger_name),
                fetch=True,
            )
        except Error as e:
            messagebox.showerror("Database error", str(e))
            return
        self.detail_text.delete("1.0", "end")
        if rows:
            self.detail_text.insert("1.0", rows[0][0])


# ------------------------------------------------------------------
# Database Info tab - shows all tables, and attributes (columns) of
# whichever table is selected
# ------------------------------------------------------------------
class DatabaseInfoTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.build_tables_list()
        self.build_attributes_view()
        self.load_tables()

    # ---- left side: list of all tables ----
    def build_tables_list(self):
        frame = ttk.LabelFrame(self, text="Tables in Database")
        frame.pack(side="left", fill="y", padx=5, pady=5)

        ttk.Button(frame, text="Refresh Tables", command=self.load_tables).pack(pady=5)

        self.tables_list = tk.Listbox(frame, width=30, height=20, exportselection=False)
        self.tables_list.pack(fill="y", padx=5, pady=5)
        self.tables_list.bind("<<ListboxSelect>>", self.on_table_selected)

    def load_tables(self):
        self.tables_list.delete(0, "end")
        try:
            rows, _ = run_query(
                """SELECT TABLE_NAME FROM information_schema.TABLES
                   WHERE TABLE_SCHEMA = %s ORDER BY TABLE_NAME""",
                (DB_CONFIG["database"],),
                fetch=True,
            )
        except Error as e:
            messagebox.showerror("Database error", str(e))
            return
        for (table_name,) in rows:
            self.tables_list.insert("end", table_name)

    # ---- right side: attributes (columns) of selected table ----
    def build_attributes_view(self):
        frame = ttk.LabelFrame(self, text="Attributes of Selected Table")
        frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.columns = ["COLUMN_NAME", "COLUMN_TYPE", "IS_NULLABLE", "COLUMN_KEY", "COLUMN_DEFAULT", "EXTRA"]
        self.attr_tree = ttk.Treeview(frame, columns=self.columns, show="headings")
        for col in self.columns:
            self.attr_tree.heading(col, text=col)
            self.attr_tree.column(col, width=130, anchor="w")
        self.attr_tree.pack(fill="both", expand=True, padx=5, pady=5)

    def on_table_selected(self, event):
        sel = self.tables_list.curselection()
        if not sel:
            return
        table_name = self.tables_list.get(sel[0])
        self.show_attributes(table_name)

    def show_attributes(self, table_name):
        for row in self.attr_tree.get_children():
            self.attr_tree.delete(row)
        try:
            rows, _ = run_query(
                """SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_KEY, COLUMN_DEFAULT, EXTRA
                   FROM information_schema.COLUMNS
                   WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                   ORDER BY ORDINAL_POSITION""",
                (DB_CONFIG["database"], table_name),
                fetch=True,
            )
        except Error as e:
            messagebox.showerror("Database error", str(e))
            return
        for row in rows:
            self.attr_tree.insert("", "end", values=row)


# ------------------------------------------------------------------
if __name__ == "__main__":
    login = LoginWindow()
    login.mainloop()