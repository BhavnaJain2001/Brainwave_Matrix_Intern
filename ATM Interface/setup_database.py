import sqlite3

# Function to set up the database
def setup_database():
    # Connect to (or create) the ATM database
    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()
    
    # Create the accounts table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            pin TEXT NOT NULL,
            balance REAL NOT NULL
        )
    ''')
    
    # Insert a test account if it doesn't already exist
    cursor.execute('''
        INSERT OR IGNORE INTO accounts (id, pin, balance) 
        VALUES (1, '1234', 1000.0)
    ''')
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Run the setup function
if __name__ == "__main__":
    setup_database()
    print("Database setup complete. Test account added if it didn't already exist.")
