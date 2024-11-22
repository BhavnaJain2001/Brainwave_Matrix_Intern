import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Database Setup
def setup_database():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')
    # Add default admin user
    cursor.execute('INSERT OR IGNORE INTO users (username, password) VALUES ("admin", "password")')
    conn.commit()
    conn.close()

# Authentication
def authenticate(username, password):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Product Management
def add_product(name, quantity, price):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
    conn.commit()
    conn.close()

def update_product(product_id, name, quantity, price):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name = ?, quantity = ?, price = ? WHERE id = ?", (name, quantity, price, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

def get_all_products():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

def get_low_stock_products(threshold=5):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE quantity < ?", (threshold,))
    low_stock = cursor.fetchall()
    conn.close()
    return low_stock

# GUI Application
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("700x500")
        self.login_screen()

    def login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Login", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.root, text="Username", font=("Arial", 12)).pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password", font=("Arial", 12)).pack(pady=5)
        self.password_entry = tk.Entry(self.root, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", font=("Arial", 12), command=self.login).pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if authenticate(username, password):
            self.main_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def main_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="Inventory Management System", font=("Arial", 18)).pack(pady=10)

        tk.Button(self.root, text="Add Product", font=("Arial", 12), command=self.add_product_screen).pack(pady=5)
        tk.Button(self.root, text="View Products", font=("Arial", 12), command=self.view_products_screen).pack(pady=5)
        tk.Button(self.root, text="Low Stock Alert", font=("Arial", 12), command=self.low_stock_alert_screen).pack(pady=5)
        tk.Button(self.root, text="Exit", font=("Arial", 12), command=self.root.quit).pack(pady=20)

    def add_product_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Add Product", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.root, text="Product Name", font=("Arial", 12)).pack(pady=5)
        self.product_name_entry = tk.Entry(self.root, font=("Arial", 12))
        self.product_name_entry.pack(pady=5)

        tk.Label(self.root, text="Quantity", font=("Arial", 12)).pack(pady=5)
        self.product_quantity_entry = tk.Entry(self.root, font=("Arial", 12))
        self.product_quantity_entry.pack(pady=5)

        tk.Label(self.root, text="Price", font=("Arial", 12)).pack(pady=5)
        self.product_price_entry = tk.Entry(self.root, font=("Arial", 12))
        self.product_price_entry.pack(pady=5)

        tk.Button(self.root, text="Add Product", font=("Arial", 12), command=self.add_product).pack(pady=20)

    def add_product(self):
        name = self.product_name_entry.get()
        quantity = int(self.product_quantity_entry.get())
        price = float(self.product_price_entry.get())
        add_product(name, quantity, price)
        messagebox.showinfo("Success", "Product added successfully!")
        self.main_menu()

    def view_products_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="All Products", font=("Arial", 18)).pack(pady=10)

        columns = ("ID", "Name", "Quantity", "Price")
        self.product_table = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.product_table.heading(col, text=col)
            self.product_table.column(col, width=150)

        self.product_table.pack(pady=10)
        self.load_products()

        tk.Button(self.root, text="Back", font=("Arial", 12), command=self.main_menu).pack(pady=20)

    def load_products(self):
        for row in self.product_table.get_children():
            self.product_table.delete(row)
        for product in get_all_products():
            self.product_table.insert("", "end", values=product)

    def low_stock_alert_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Low Stock Alert", font=("Arial", 18)).pack(pady=10)

        low_stock_products = get_low_stock_products()
        if low_stock_products:
            for product in low_stock_products:
                tk.Label(self.root, text=f"{product[1]}: {product[2]} items left", font=("Arial", 12)).pack(pady=5)
        else:
            tk.Label(self.root, text="No low stock items!", font=("Arial", 12)).pack(pady=5)

        tk.Button(self.root, text="Back", font=("Arial", 12), command=self.main_menu).pack(pady=20)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run Application
if __name__ == "__main__":
    setup_database()
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
