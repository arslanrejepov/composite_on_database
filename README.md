# Online Store DB System

## Setup

1. **Install the dependencies** 

```
   python -m venv .venv

   .venv\Scripts\activate for Windows  
   source .venv/bin/activate for MacOS/Linux

   pip install mysql-connector-python
   
   python store_gui.py

   deactivate
```


2. **Edit your database connection** in `db/connection.py`:
   ```python
   DB_CONFIG = {
       "host": "localhost",
       "port": 3306,
       "user": "root",
       "password": "YOUR_PASSWORD",
       "database": "onlinestoredb_046",
   }
   ```
   This is the ONLY file you need to change to point the app at your MySQL database.

3. Run your existing DDL (tables, views, triggers, indexes) against MySQL to create
   the `online_store` database — either paste it into `db/schema.sql` and run it, or
   run your existing .sql script directly in MySQL Workbench / CLI.


## Structure

- `db/connection.py` — **edit this for your DB credentials**
- `db/schema.sql` — paste your CREATE TABLE/VIEW/TRIGGER/INDEX SQL here
- `models/` — one file per table, holds all SQL queries (CRUD)
- `ui/` — one window per role (Customer, Manager, Cashier, Inventory Clerk)
- `main.py` — run this to start the app

## Next steps

- Fill in each `ui/*.py` file with a table/list widget and buttons wired to the
  matching functions in `models/*.py`.
- Views (cashier product view, sales stats view, member discount view) are just
  SELECTs against your SQL views — call them the same way as `get_all_available_products()`
  in `models/product.py`.
- Take screenshots of each working function for your report as you go.

System Demonstration:
The Online Store Management System was implemented as a Python/Tkinter desktop application connected to the OnlineStoreDB_046 MySQL database. The application demonstrates all required CRUD operations, views, and triggers through five functional modules (tabs), accessible after authenticating against the Users_046 table.
1. Login
On launch, the user is prompted for a username and password, which are validated against the Users_046 table (role: Manager, Cashier, or Inventory Clerk). This demonstrates a basic SELECT query with a WHERE clause on two columns and simulates role-based system access.
2. Products Tab
Displays the full product catalog joined with category name and live stock quantity (a 3-table JOIN across Products_046, Categories_046, and Inventory_046). Staff can search products by name and add new products through a form, which inserts into Products_046 and simultaneously creates the corresponding Inventory_046 record — demonstrating Create and Read operations across two related tables in a single transaction.
3. Inventory Tab
Lists current stock levels and reorder thresholds for every product. A "Show Low Stock Only" button filters to items where stock_quantity is below reorder_level, giving the Inventory Clerk an at-a-glance view of what needs restocking. This tab is directly linked to the low-stock warning trigger: whenever an order reduces a product's stock below its threshold, the resulting warning is visible here.
Login:
|_______________________________|
|Username     |	Password      |
|manager1	  |   manager123    |
|cashier1	  |   cashier123    |
|inventory1   |	inventory123  |
|———————————————————————————————|

 
Insert information then click Login.
Usage Guide
1.	Products — Browse/search products. Click a row to auto-fill the edit form; update price/discount/status or delete. Use the top form to add a new product (also creates its inventory row).
 
2.	Inventory — View stock levels. "Show Low Stock Only" filters items below reorder level. Click a row to auto-fill the update form, then adjust stock quantity / reorder level and save.
 
click Show Low Stock Only  to display products with the less count then using functions below we can update the Quantity
3.	Customers — Browse/search customers. Click a row to edit phone/membership or delete. Use the top form to add a new customer.

4.	Orders — View all orders with customer names. Enter an Order ID and pick a new status to update it (marking "Completed" auto-awards loyalty points via trigger).

5.	Place Order — Pick a customer, add products to a cart with quantities, review the cart/total, then submit — creates the order and deducts stock automatically.
 
6.	Views — Pick one of the three SQL views from the dropdown and click "Load View" to see its results (available products, sales totals, discounted items).
 
7.	Triggers — Lists all triggers on the database. Click one to see its full SQL body in the box below.
 
8.	Database Info — Left panel lists all tables. Click a table name to see its columns/attributes on the right (type, nullable, key, default).
 

