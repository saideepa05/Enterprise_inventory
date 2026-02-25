import pandas as pd
import sqlite3
import os

def init_db():
    # Load the downloaded CSV
    if not os.path.exists("diamonds.csv"):
        print("Error: diamonds.csv not found.")
        return

    df = pd.read_csv("diamonds.csv")
    
    # Create the SQLite connection
    conn = sqlite3.connect("inventory.db")
    
    # Write the data to a table called 'inventory'
    df.to_sql("inventory", conn, if_exists="replace", index=False)
    
    print("Database 'inventory.db' initialized with 'inventory' table.")
    
    # Verify
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM inventory")
    count = cursor.fetchone()[0]
    print(f"Total records in inventory: {count}")
    
    conn.close()

if __name__ == "__main__":
    init_db()
