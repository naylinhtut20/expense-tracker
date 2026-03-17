import os
import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self, data_file_path):
        self.data_file_path =  data_file_path
        self.expenses = []
        self.load_expenses()

    def load_expenses(self):
        if not os.path.exists(self.data_file_path):
            self.expenses = []
            return

        with open(self.data_file_path, "r") as file:
            try:
                self.expenses = json.load(file)
            except json.JSONDecodeError:
                self.expenses = []

    def sort_expenses_by_date(self):
        self.expenses.sort(
            key=lambda expense: datetime.strptime(expense["date"], "%Y-%m-%d")
        )

    def save_expenses(self):
        with open(self.file_name, "w") as file:
            json.dump(self.expenses, file, indent=4)

    def has_expenses(self):
        if not self.expenses:
            print("No expneses found.")
            return False
        return True

    def add_expense(self):
        expense_record = {
            "amount": get_amount(),
            "category": get_category(),
            "description": get_description(),
            "date": get_date()
        }

        self.expenses.append(expense_record)
        self.save_expenses()
        print("Expense added successfully!")

    def view_expense(self):
        self.sort_expenses_by_date()

        if not self.has_expenses():
            return

        for index, expense in enumerate(self.expenses, start=1):
            print(f"{index}. Amount: ${expense['amount']}")
            print(f"   Category: {expense['category']}")
            print(f"   Description: {expense['description']}")
            print(f"   Date: {expense['date']}")
            print()

    def delete_expense(self):
        self.view_expense()

        if not self.has_expenses():
            return

        selection = input("Enter the expense number to delete: ")

        if not selection.isdigit():
            print("Invalid number.")
            return

        expense_index = int(selection) - 1

        if 0 <= expense_index < len(self.expenses):
            self.expenses.pop(expense_index)
            self.save_expenses()
            print("Expense deleted successfully.")
        else:
            print("Invalid selection.")

    def view_total_spending(self):
        if not self.has_expenses():
            return
        
        total_spending = 0

        for expense in self.expenses:
            total_spending += float(expense.get("amount", 0))

        print(f"Total spending: ${total_spending}")

    def view_spending_by_category(self):
        if not self.has_expenses():
            return
        
        category_totals = {}

        for expense in self.expenses:
            category_name = expense["category"]
            amount = float(expense["amount"])

            if category_name in category_totals:
                category_totals[category_name] += amount
            else:
                category_totals[category_name] = amount

        print("\nSpending by Category:")
        for category_name, total_amount in category_totals.items():
            print(f"{category_name}: ${total_amount}")

    def view_highest_expense(self):
        if not self.has_expenses():
            return

        highest_expense = max(self.expenses, key=lambda expense: float(expense["amount"]))

        print("\nHighest Expense: ")
        print(
            f"${highest_expense['amount']} - {highest_expense['category']} - {highest_expense['date']}"
            )

    def view_lowest_expense(self):
        if not self.has_expenses():
            return

        lowest_expense = min(self.expenses, key=lambda expense: float(expense["amount"]))

        print("\nLowest Expense:")

        print(
            f"${lowest_expense['amount']} - {lowest_expense['category']} - {lowest_expense['date']}"
            )

    def edit_expense(self):
        self.view_expense()

        if not self.has_expenses():
            return
        
        selection = input("Enter the expense number to edit: ")

        if not selection.isdigit():
            print("Invalid number.")
            return
        
        expense_index = int(selection) - 1

        if 0 <= expense_index < len(self.expenses):

            updated_amount = get_amount()
            updated_category = get_category()
            updated_description = get_description()
            updated_date = get_date()

            self.expenses[expense_index]["amount"] = updated_amount
            self.expenses[expense_index]["category"] = updated_category
            self.expenses[expense_index]["description"] = updated_description
            self.expenses[expense_index]["date"] = updated_date

            print("Expense updated successfully!")
            self.save_expenses()
        else:
            print("Invalid number")

    def monthly_spending_summary(self):
        if not self.has_expenses():
            return

        target_month = input("Enter month (YYYY-MM): ")

        monthly_total =  0
        category_totals = {}

        for expense in self.expenses:
            if expense["date"].startswith(target_month):
                amount = float(expense["amount"])
                monthly_total += amount

                category_name = expense["category"]

                if category_name in category_totals:
                    category_totals[category_name] += amount
                else:
                    category_totals[category_name] = amount

        print(f"\nTotal spending: for {target_month}: ${monthly_total}")

        print("\nSpending by category:")
        for category_name, amount in category_totals.items():
            print(f"{category_name}: ${amount}")

# ---- amount ----
def get_amount():
    while True:
        amount_text = get_non_empty_input("Enter amount: ")
        if amount_text.replace(".", "", 1).isdigit():
            return float(amount_text)
        print("Invalid amount. Please enter a number.")

# ---- category ----
def get_category():
    return get_non_empty_input("Enter category: ")

# ---- description ----
def get_description():
    return get_non_empty_input("Enter description: ")

# ---- date ----
def get_date():
    while True:
        print("Enter date:")
        day_text = get_non_empty_input("Date: ")
        month_text = get_non_empty_input("Month: ")
        year_text = get_non_empty_input("Year: ")

        if not (day_text.isdigit() and month_text.isdigit() and year_text.isdigit()):
            print("Date values must be numbers.")
            continue
        
        current_year = datetime.now().year

        if not (2000 <= int(year_text) <= current_year):
            print(f"Year must be between 2000 and {current_year}")
            continue

        try:
            valid_date = datetime(int(year_text), int(month_text), int(day_text))
            date = valid_date.strftime("%Y-%m-%d")
            return date
        except ValueError:
            print("Invalid date. Please enter a real calendar date.")

def get_non_empty_input(prompt_message):
    while True:
        user_input = input(prompt_message).strip()
        if user_input:
            return user_input
        print("Input cannot be empty.")

def main():
    tracker = ExpenseTracker("expense.json")

    while True:
        print("\nExpense Tracker Menu")
        print("1. Add an expenses")
        print("2. View all expenses")
        print("3. View total spending")
        print("4. View spending by category")
        print("5. View highest and lowest expense")
        print("6. Delete an expense")
        print("7. Edit an expense")
        print("8. View monthly spending summary")
        print("Q. Quit")

        choice = input("Select an option: ").strip().lower()

        match choice:
            case "1":
                tracker.add_expense()
            
            case "2":
                tracker.view_expense()
            
            case "3":
                tracker.view_total_spending()
            
            case "4":
                tracker.view_spending_by_category()
            
            case "5":
                tracker.view_highest_expense()
                tracker.view_lowest_expense()
            
            case "6":
                tracker.delete_expense()
            
            case "7":
                tracker.edit_expense()
            
            case "8":
                tracker.monthly_spending_summary()
            
            case "q" | "quit" | "exit":
                print("Goodbye!")
                break

            case _:
                print("Invalid choice. Please try again.")


if "__main__" == __name__:
    main()