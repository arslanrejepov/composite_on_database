# Online Store DB System

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
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

4. Test the connection:
   ```
   python db/connection.py
   ```
   You should see: `✅ Connected successfully to: online_store`

5. Run the app:
   ```
   python main.py
   ```

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
