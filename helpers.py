import sqlite3
import datetime

def init_db(): 
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS income (income_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, amount REAL NOT NULL, date TEXT NOT NULL, FOREIGN KEY (user_id) REFERENCES users(user_id))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS expenses (expense_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, category TEXT NOT NULL, amount REAL NOT NULL, date TEXT NOT NULL, FOREIGN KEY (user_id) REFERENCES users(user_id))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS savings_goal (user_id INTEGER PRIMARY KEY, amount REAL NOT NULL, FOREIGN KEY (user_id) REFERENCES users(user_id))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS recurring_expenses (recurring_expense_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, category TEXT NOT NULL, amount REAL NOT NULL, frequency TEXT NOT NULL, FOREIGN KEY (user_id) REFERENCES users(user_id))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, hash TEXT NOT NULL)""")
   
    conn.commit()
    conn.close()


def apply_recurring_expenses():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

 
    current_date = datetime.date.today()
    current_month = current_date.month
    current_year = current_date.year

    cursor.execute("SELECT COUNT(*) FROM expenses WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?",
                   (f"{current_month:02d}", str(current_year)))
    expenses_exist = cursor.fetchone()[0] > 0

    if not expenses_exist:
        cursor.execute("SELECT category, amount FROM recurring_expenses WHERE frequency = 'monthly'")
        for category, amount in cursor.fetchall():
            cursor.execute("INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)",
                           (category, amount, current_date.isoformat()))

    conn.commit()
    conn.close()

