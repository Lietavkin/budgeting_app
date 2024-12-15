from flask import Flask, render_template, request, redirect
import sqlite3
from helpers import init_db
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
init_db()

@app.route("/")
def home():
    return render_template("/home.html")  

@app.route("/input")
def input_form():
    return render_template("income_expense.html")

@app.route("/savings_goal", methods=["POST"])
def savings_goal():
    savings_goal= float(request.form.get("savings_goal"))
    conn=sqlite3.connect("database.db")
    cursor=conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO savings_goal(id,amount) VALUES(?,?)",(1, savings_goal))
    conn.commit()
    conn.close()
    return redirect("/dashboard")

@app.route("/add_income", methods=["POST"])
def add_income():
    income = request.form["income"]
    date = request.form["income_date"]
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO income (amount, date) VALUES (?, ?)", (income, date))
    conn.commit()
    conn.close()
    return redirect("/input")

@app.route("/add_expense", methods=["POST"])
def add_expense():
    category = request.form["category"]
    expense = request.form["expense"]
    date = request.form["expense_date"]
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)", (category, expense, date))
    conn.commit()
    conn.close()
    return redirect("/input")

@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM income")
    total_income= cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_expenses = cursor.fetchone()[0] or 0
    cursor.execute("SELECT amount from savings_goal WHERE id=?",(1,))
    savings_goal = cursor.fetchone()
    savings_goal=savings_goal[0] if savings_goal else 0

    total_savings = total_income - total_expenses

    suggestions= []
    if total_savings < savings_goal:
        deficit = savings_goal - total_savings
        suggestions.append(f"You are ${deficit:.2f} short of your savings goal! Maybe you should consider mitigating your expenses.")
    else:
        suggestions.append(f"You are doing a great job meeting your savings goal of {savings_goal}!")

    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    expense_summary= {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()

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

    plt.figure(figsize=(6,4))
    categories = ["Income","Expenses"]
    amounts = [total_income, total_expenses]
    plt.bar(categories, amounts, color=(["green","red"]))
    plt.title("Income vs Expenses")
    plt.ylabel("Amount($)")
    plt.tight_layout()

    bar_chart_path = os.path.join("static", "income_vs_expenses.png")
    if os.path.exists(bar_chart_path):
        os.remove(bar_chart_path)
    plt.savefig(bar_chart_path)
    plt.close()

    return render_template("dashboard.html", savings_goal=savings_goal, suggestions = suggestions, total_income=total_income,total_expenses=total_expenses, total_savings=total_savings, expense_summary=expense_summary, chart_path=chart_path, bar_chart_path=bar_chart_path)








if __name__ == '__main__':
    print("starting app")
    app.run(debug=True)
