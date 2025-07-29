import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from expense import Expense
import calendar
import datetime
from datetime import date
from typing import List

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f8ff")
        self.budget = 0
        self.expense_file_path = "expenses.csv"

        self.welcome_window()

    def welcome_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root, text="Welcome to Expense Tracker", font=("Helvetica", 20, "bold"), bg="#f0f8ff"
        ).pack(pady=20)

        tk.Label(self.root, text="Enter Your Name:", bg="#f0f8ff").pack(pady=5)
        name_entry = ttk.Entry(self.root)
        name_entry.pack(pady=5)

        tk.Label(self.root, text="Enter Initial Budget:", bg="#f0f8ff").pack(pady=5)
        budget_entry = ttk.Entry(self.root)
        budget_entry.pack(pady=5)

        def proceed():
            name = name_entry.get().strip()
            budget = budget_entry.get().strip()
            
            if not name or not budget:
                messagebox.showwarning("Input Error", "Both fields are required!")
                return
            
            try:
                self.user_name = name
                self.budget = float(budget)
                messagebox.showinfo("Welcome", f"Welcome, {self.user_name}!")
                self.main_menu()
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid budget.")

        ttk.Button(self.root, text="Proceed", command=proceed).pack(pady=20)

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        

        label = tk.Label(
            self.root, text="Expense Tracker", font=("Helvetica", 24, "bold"), bg="#f0f8ff"
        )
        label.pack(pady=20)

        options = [
            ("Add Expense", self.add_expense_window),
            ("View Expenses", self.view_expenses_window),
            ("Delete Expense", self.delete_expense_window),
            ("Summarize Expenses", self.summarize_expenses_window),
            ("Change Budget", self.change_budget_window),
        ]

        for text, command in options:
            btn = ttk.Button(self.root, text=text, command=command)
            btn.pack(pady=5, ipadx=10, ipady=5)

    def add_expense_window(self):
        self.switch_window("Add Expense", self.add_expense_content)

    def add_expense_content(self, frame):
        tk.Label(frame, text="Expense Name:").grid(row=0, column=0, pady=5)
        name_entry = ttk.Entry(frame)
        name_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Amount:").grid(row=1, column=0, pady=5)
        amount_entry = ttk.Entry(frame)
        amount_entry.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Category:").grid(row=2, column=0, pady=5)
        category_var = tk.StringVar()
        categories = ["🍔 Food", "🏠 Home", "💼 Work", "🎉 Fun", "✨ Misc"]

        category_dropdown = ttk.Combobox(frame, values=categories, textvariable=category_var)
        category_dropdown.grid(row=2, column=1, pady=5)

        def save_expense():
            name = name_entry.get()
            amount = amount_entry.get()
            category = category_var.get()

            if not name or not amount or not category:
                messagebox.showwarning("Input Error", "All fields are required!")
                return

            try:
                expense = Expense(name=name, amount=float(amount), category=category)
                with open(self.expense_file_path, "a", encoding="utf-8") as f:
                    f.write(f"{expense.name},{expense.amount},{expense.category},{date.today().strftime("%B")}\n")
                messagebox.showinfo("Success", "Expense added successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(frame, text="Save Expense", command=save_expense).grid(row=3, column=0, columnspan=2, pady=10)

    def view_expenses_window(self):
        self.switch_window("View Expenses", self.view_expenses_content)

    def view_expenses_content(self, frame):
        try:
            with open(self.expense_file_path, "r", encoding="utf-8") as f:
                expenses = f.readlines()

            if not expenses:
                tk.Label(frame, text="No expenses to display!", fg="red").pack(pady=20)
            else:
                for idx, expense in enumerate(expenses):
                    tk.Label(frame, text=f"{idx + 1}. {expense.strip()}").pack(anchor="w")
        except FileNotFoundError:
            tk.Label(frame, text="No expenses file found!", fg="red").pack(pady=20)

    def delete_expense_window(self):
        self.switch_window("Delete Expense", self.delete_expense_content)

    def delete_expense_content(self, frame):
        try:
            with open(self.expense_file_path, "r", encoding="utf-8") as f:
                expenses = f.readlines()

            if not expenses:
                tk.Label(frame, text="No expenses to delete!", fg="red").pack(pady=20)
                return

            listbox = tk.Listbox(frame)
            listbox.pack(fill="both", expand=True, pady=10)
            for expense in expenses:
                listbox.insert("end", expense.strip())

            def delete_selected():
                selected_idx = listbox.curselection()
                if not selected_idx:
                    messagebox.showwarning("Selection Error", "No expense selected!")
                    return

                expenses.pop(selected_idx[0])
                with open(self.expense_file_path, "w", encoding="utf-8") as f:
                    f.writelines(expenses)
                messagebox.showinfo("Success", "Expense deleted successfully!")
                self.delete_expense_window()

            ttk.Button(frame, text="Delete Selected", command=delete_selected).pack(pady=10)

        except FileNotFoundError:
            tk.Label(frame, text="No expenses file found!", fg="red").pack(pady=20)

    def summarize_expenses_window(self):
        self.switch_window("Summarize Expenses", self.summarize_expenses_content)

    def summarize_expenses_content(self, frame):
        try:
            with open(self.expense_file_path, "r", encoding="utf-8") as f:
                expenses = f.readlines()

            amount_by_category = {}
            total_spent = 0

            for line in expenses:
                _, amount, category,spent_mon= line.strip().split(",")
                amount = float(amount)
                total_spent += amount
                if category in amount_by_category:
                    amount_by_category[category] += amount
                else:
                    amount_by_category[category] = amount

            for category, amount in amount_by_category.items():
                tk.Label(frame, text=f"Spent on{category}: \u20B9{amount:.2f}").pack(anchor="w",pady=5)
            amount_by_month= {}
            total_monthly_spent = 0

            for line in expenses:
                _, amount, category,spent_mon= line.strip().split(",")
                amount = float(amount)
                total_monthly_spent += amount
                if spent_mon in amount_by_month:
                    amount_by_month[spent_mon] += amount
                else:
                     amount_by_month[spent_mon]  = amount

            for spent_mon, amount in amount_by_month.items():
                tk.Label(frame, text=f"Spent in Month {spent_mon}: \u20B9{amount:.2f}").pack(anchor="w",pady=5)

            tk.Label(frame, text=f"💵 Total Spent: \u20B9{total_spent:.2f}").pack(anchor="w", pady=10)
            tk.Label(frame, text=f"✅ Remaining Budget: \u20B9{self.budget - total_spent:.2f}").pack(anchor="w")
        except FileNotFoundError:
            tk.Label(frame, text="No expenses file found!", fg="red").pack(pady=20)
        now = datetime.datetime.now()
        days_in_month = calendar.monthrange(now.year, now.month)[1]
        remaining_days = days_in_month - now.day

        daily_budget = self.budget - total_spent / remaining_days
        tk.Label(frame,text="👉 Budget Per Day: \u20B9{daily_budget:.2f}")


    def change_budget_window(self):
        self.switch_window("Change Budget", self.change_budget_content)

    def change_budget_content(self, frame):
        tk.Label(frame, text="Enter New Budget:").pack(pady=5)
        budget_entry = ttk.Entry(frame)
        budget_entry.pack(pady=5)

        def save_budget():
            try:
                self.budget = int(budget_entry.get())
                messagebox.showinfo("Success", "Budget updated successfully!")
            except ValueError:
                messagebox.showwarning("Input Error", "Please enter a valid number.")

        ttk.Button(frame, text="Save Budget", command=save_budget).pack(pady=10)

    def switch_window(self, title, content_func):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=title, font=("Helvetica", 18, "bold"), bg="#f0f8ff").pack(pady=10)
        frame = tk.Frame(self.root, bg="#f0f8ff")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        content_func(frame)

        ttk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()





