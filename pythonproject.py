import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt

# ----------------------- Expense Tracker Class -----------------------
class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker with Visualization")
        self.root.geometry("800x600")
        self.expenses = []  # List to store all expenses

        # -------------------- UI Setup --------------------
        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self.root, text="💰 Expense Tracker", font=("Arial", 20, "bold"), fg="#2c3e50")
        title.pack(pady=10)

        # Input Frame
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Category:").grid(row=0, column=0, padx=5, pady=5)
        self.category_entry = tk.Entry(frame)
        self.category_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Amount:").grid(row=0, column=2, padx=5, pady=5)
        self.amount_entry = tk.Entry(frame)
        self.amount_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=0, column=4, padx=5, pady=5)
        self.date_entry = tk.Entry(frame)
        self.date_entry.grid(row=0, column=5, padx=5, pady=5)

        add_button = tk.Button(frame, text="Add Expense", command=self.add_expense, bg="#27ae60", fg="white")
        add_button.grid(row=0, column=6, padx=10, pady=5)

        # Treeview for expense table
        self.tree = ttk.Treeview(self.root, columns=("Category", "Amount", "Date"), show='headings')
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Date", text="Date")
        self.tree.pack(pady=10, fill="x", padx=20)

        # Visualization Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Show Pie Chart", command=self.show_pie_chart, bg="#2980b9", fg="white", width=15).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Show Bar Graph", command=self.show_bar_chart, bg="#8e44ad", fg="white", width=15).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="Clear All", command=self.clear_all, bg="#c0392b", fg="white", width=15).grid(row=0, column=2, padx=10)

    # ----------------------- Add Expense -----------------------
    def add_expense(self):
        category = self.category_entry.get().strip()
        amount = self.amount_entry.get().strip()
        date = self.date_entry.get().strip()

        if not category or not amount:
            messagebox.showerror("Input Error", "Please enter both category and amount!")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a number!")
            return

        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        self.expenses.append({"category": category, "amount": amount, "date": date})
        self.tree.insert("", "end", values=(category, amount, date))
        self.clear_inputs()

    # ----------------------- Clear Inputs -----------------------
    def clear_inputs(self):
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)

    # ----------------------- Clear All -----------------------
    def clear_all(self):
        self.expenses.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)

    # ----------------------- Pie Chart -----------------------
    def show_pie_chart(self):
        if not self.expenses:
            messagebox.showinfo("No Data", "No expenses to display.")
            return

        category_totals = {}
        for exp in self.expenses:
            category_totals[exp["category"]] = category_totals.get(exp["category"], 0) + exp["amount"]

        plt.figure(figsize=(6, 6))
        plt.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%', startangle=90)
        plt.title("Expense Distribution by Category")
        plt.show()

    # ----------------------- Bar Chart -----------------------
    def show_bar_chart(self):
        if not self.expenses:
            messagebox.showinfo("No Data", "No expenses to display.")
            return

        category_totals = {}
        for exp in self.expenses:
            category_totals[exp["category"]] = category_totals.get(exp["category"], 0) + exp["amount"]

        categories = list(category_totals.keys())
        amounts = list(category_totals.values())

        plt.figure(figsize=(8, 5))
        plt.bar(categories, amounts)
        plt.xlabel("Category")
        plt.ylabel("Total Amount")
        plt.title("Expenses by Category")
        plt.show()


# ----------------------- Main Execution -----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
    
