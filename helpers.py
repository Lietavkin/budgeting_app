import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute(""" CREATE TABLE IF NOT EXISTS income (id INTEGER PRIMARY KEY AUTOINCREMENT,amount REAL NOT NULL,date TEXT NOT NULL ) """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS expenses ( id INTEGER PRIMARY KEY AUTOINCREMENT,category TEXT NOT NULL, amount REAL NOT NULL,date TEXT NOT NULL)""")
    conn.commit()
    conn.close()
