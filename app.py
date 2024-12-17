from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3
from helpers import init_db, apply_recurring_expenses
import matplotlib.pyplot as plt
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets




app = Flask(__name__)

app.secret_key = secrets.token_hex(16)
init_db()
apply_recurring_expenses()

@app.route("/")
def home():
    if "user_id"  not in session: 
        return redirect('/login')  
    return redirect('/dashboard')  


@app.route("/input")
def input_form():
    if 'user_id' not in session:  # Check if the user is not logged in
        return redirect('/login')  
    user_id = session["user_id"]
    return render_template("income_expense.html")

@app.route("/savings_goal", methods=["POST"])
def savings_goal():
    try:
        savings_goal= float(request.form.get("savings_goal"))
        if savings_goal <=0:
            raise ValueError("Savings goal must be a positive number!")
        conn=sqlite3.connect("database.db")
        cursor=conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO savings_goal(id,amount) VALUES(?,?)",(1, savings_goal))
        conn.commit()
        conn.close()
        return redirect("/dashboard")
    except ValueError as e:
        return f"<h1>Error: {str(e)}</h1><a href='/input'>Go back</a>", 400

@app.route("/add_income", methods=["POST"])
def add_income():
    try:
        income = float(request.form["income"])
        if income < 0:
            raise ValueError("Income must be a positive number")
        date = request.form["income_date"]
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO income (amount, date) VALUES (?, ?)", (income, date))
        conn.commit()
        conn.close()
        return redirect("/input")
    except ValueError as e:
        return f"<h1>Error: {str(e)}</h1><a href='/input'>Go back</a>"

@app.route("/add_expense", methods=["POST"])
def add_expense():
    try:
        expense = float(request.form["expense"])
        if expense < 0:
            raise ValueError("Expense must be a positive number")
        category = request.form["category"]
        date = request.form["expense_date"]
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)", (category, expense, date))
        conn.commit()
        conn.close()
        return redirect("/input")
    except ValueError as e:
        return f"<h1>Error: {str(e)}</h1><a href='/input'>Go back</a>"
    
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login") 
    user_id = session["user_id"]
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM income WHERE user_id=?",(user_id,))
    total_income= cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id=?",(user_id,))
    total_expenses = cursor.fetchone()[0] or 0
    cursor.execute("SELECT amount from savings_goal WHERE user_id=?",(user_id,))
    savings_goal = cursor.fetchone()
    savings_goal=savings_goal[0] if savings_goal else 0

    total_savings = total_income - total_expenses

    cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE user_id=? GROUP BY category ",(user_id,))
    expense_summary= {row[0]: row[1] for row in cursor.fetchall()}
    

    if expense_summary:
        values = list(expense_summary.values())
        labels = list(expense_summary.keys())
        plt.figure(figsize=(6, 6))
        plt.pie(values, labels = labels, autopct="%1.1f%%", startangle = 140)
        plt.title("Expense breakdown by category")
        os.makedirs("static", exist_ok=True)
        chart_path=os.path.join("static", "expense_pie_chart.png")
        if os.path.exists(chart_path):
            os.remove(chart_path)
        plt.savefig(chart_path)
        plt.close()
    else:
        chart_path= None

    if total_income == 0 and total_expenses == 0:
        bar_chart_path = None
    else:
        plt.figure(figsize=(6,4))
        categories = ["Income","Expenses"]
        amounts = [total_income, total_expenses]
        plt.bar(categories, amounts, color=["green","red"])
        plt.title("Income vs Expenses")
        plt.ylabel("Amount($)")
        plt.tight_layout()

        bar_chart_path = os.path.join("static", "income_vs_expenses.png")
        if os.path.exists(bar_chart_path):
            os.remove(bar_chart_path)
        plt.savefig(bar_chart_path)
        plt.close()

    cursor.execute("SELECT category, amount, frequency FROM recurring_expenses  WHERE user_id = ?", (user_id,))
    recurring_expenses = [{"category": row[0], "amount": row[1], "frequency": row[2]} for row in cursor.fetchall()]
    
    

    suggestions= []
    if total_income == 0 and total_expenses == 0:
        suggestions.append("No data to show.")
    elif total_savings < savings_goal:
        deficit = savings_goal - total_savings
        suggestions.append(f"You are ${deficit:.2f} short of your savings goal! Maybe you should consider reducing your expenses.")
    else:
        suggestions.append(f"You are doing a great job meeting your savings goal of ${savings_goal}!")
    conn.close()
    return render_template ("dashboard.html", recurring_expenses= recurring_expenses, savings_goal=savings_goal, suggestions = suggestions, total_income=total_income,total_expenses=total_expenses, total_savings=total_savings, expense_summary=expense_summary, chart_path=chart_path, bar_chart_path=bar_chart_path)



@app.route("/report")
def report_page():
    return render_template("report.html")


@app.route("/create_report")
def create_report():
    report_path = "static/financial_report.pdf"
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT sum(amount) FROM income")
    total_income = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_expenses= cursor.fetchone()[0] or 0

    cursor.execute("SELECT amount FROM savings_goal WHERE user_id = user_id")
    savings_goal = cursor.fetchone()
    savings_goal = savings_goal[0] if savings_goal else 0

    total_savings = total_income - total_expenses
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    expense_summary = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()

    c = canvas.Canvas(report_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Financial Report")
    c.drawString(50, 700, f"Total Income: ${total_income:.2f}")
    c.drawString(50, 680, f"Total Expenses: ${total_expenses:.2f}")
    c.drawString(50, 660, f"Remaining Savings: ${total_savings:.2f}")
    c.drawString(50, 640, f"Savings Goal: ${savings_goal:.2f}")
    c.drawString(50, 600, "Expense Breakdown by Category:")
    y = 580
    for category, amount in expense_summary:
        c.drawString(70, y, f"{category}: ${amount:.2f}")
        y -= 20
        
    c.save()
    return send_file(report_path, as_attachment=True)


@app.route("/recurring_expenses", methods=["POST"])
def recurring_expenses():
    try:
        category = request.form.get("category")
        amount= float(request.form.get("amount"))
        frequency= request.form.get("frequency")
        if amount <= 0:
            return "Amount must be a positive number"
        conn = sqlite3.connect("database.db")
        cursor= conn.cursor()
        cursor.execute("INSERT INTO recurring_expenses (category, amount, frequency) VALUES (?, ?, ?)",(category, amount, frequency))
        conn.commit()
        conn.close()
        return redirect("/input")
    except ValueError as r:
        return f"<h1>Error: {str(r)}</h1><a href='/input'>Go back<a>",400


@app.route("/history")
def history():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT strftime("%Y-%m", date) AS month, SUM(amount) FROM income GROUP BY month ORDER BY month DESC""")
    income_history = cursor.fetchall()

    cursor.execute("""SELECT strftime("%Y-%m", date) AS month, SUM(amount) FROM expenses GROUP BY month ORDER BY month DESC""")
    expense_history = cursor.fetchall()
    conn.close()

   
    history = {}
    for month, income in income_history:
        history[month] = {"income": income, "expenses": 0}
    for month, expenses in expense_history:
        if month in history:
            history[month]["expenses"] = expenses
        else:
            history[month] = {"income": 0, "expenses": expenses}

    return render_template("history.html", history=history)

        
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hash_password = generate_password_hash(password)
        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash_password))
            conn.commit()
            conn.close()
            return redirect("/login")
        except sqlite3.IntegrityError:
            return "Username already exists. Please try again."
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, hash FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0] 
            return redirect("/")
        else:
            return "Invalid username or password."
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    print("starting app")
    app.run(debug=True)
