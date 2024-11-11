
import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database Setup
def setup_database():
    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                        id INTEGER PRIMARY KEY,
                        pin TEXT,
                        balance REAL
                     )''')
    # Insert a test account if it doesn't exist
    cursor.execute('''INSERT OR IGNORE INTO accounts (id, pin, balance) 
                      VALUES (1, '1234', 1000.0)''')
    conn.commit()
    conn.close()

# Function to check PIN
def check_pin(pin):
    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts WHERE pin = ?", (pin,))
    account = cursor.fetchone()
    conn.close()
    return account

# Function to retrieve balance
def get_balance(account_id):
    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
    balance = cursor.fetchone()[0]
    conn.close()
    return balance

# Function to update balance
def update_balance(account_id, new_balance):
    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_balance, account_id))
    conn.commit()
    conn.close()

# ATM Application class
class ATMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Interface")
        self.root.geometry("400x300")
        
        self.account_id = None
        self.login_screen()

    def login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Enter PIN:", font=("Arial", 14)).pack(pady=10)
        self.pin_entry = tk.Entry(self.root, font=("Arial", 14), show="*")
        self.pin_entry.pack(pady=5)
        tk.Button(self.root, text="Login", font=("Arial", 14), command=self.check_login).pack(pady=10)

    def check_login(self):
        pin = self.pin_entry.get()
        account = check_pin(pin)
        if account:
            self.account_id = account[0]
            self.main_menu()
        else:
            messagebox.showerror("Error", "Invalid PIN")

    def main_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="ATM Main Menu", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="View Balance", font=("Arial", 14), command=self.view_balance).pack(pady=5)
        tk.Button(self.root, text="Deposit", font=("Arial", 14), command=self.deposit_screen).pack(pady=5)
        tk.Button(self.root, text="Withdraw", font=("Arial", 14), command=self.withdraw_screen).pack(pady=5)
        tk.Button(self.root, text="Exit", font=("Arial", 14), command=self.root.quit).pack(pady=10)

    def view_balance(self):
        balance = get_balance(self.account_id)
        messagebox.showinfo("Balance", f"Your current balance is ${balance:.2f}")

    def deposit_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Enter Deposit Amount:", font=("Arial", 14)).pack(pady=10)
        self.amount_entry = tk.Entry(self.root, font=("Arial", 14))
        self.amount_entry.pack(pady=5)
        tk.Button(self.root, text="Deposit", font=("Arial", 14), command=self.deposit).pack(pady=10)

    def deposit(self):
        amount = float(self.amount_entry.get())
        current_balance = get_balance(self.account_id)
        new_balance = current_balance + amount
        update_balance(self.account_id, new_balance)
        messagebox.showinfo("Deposit", f"${amount:.2f} deposited successfully!")
        self.main_menu()

    def withdraw_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Enter Withdraw Amount:", font=("Arial", 14)).pack(pady=10)
        self.amount_entry = tk.Entry(self.root, font=("Arial", 14))
        self.amount_entry.pack(pady=5)
        tk.Button(self.root, text="Withdraw", font=("Arial", 14), command=self.withdraw).pack(pady=10)

    def withdraw(self):
        amount = float(self.amount_entry.get())
        current_balance = get_balance(self.account_id)
        if amount <= current_balance:
            new_balance = current_balance - amount
            update_balance(self.account_id, new_balance)
            messagebox.showinfo("Withdraw", f"${amount:.2f} withdrawn successfully!")
        else:
            messagebox.showerror("Error", "Insufficient balance")
        self.main_menu()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Initialize database and run application
setup_database()
root = tk.Tk()
app = ATMApp(root)
root.mainloop()