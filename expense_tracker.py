import os
import json
from datetime import datetime

class ExpenseTracker:
    """Store, display, and manage expense records saved in a JSON file."""

    def __init__(self, data_file_path: str):
        """Initialize the tracker and load saved expenses from disk."""
        self.data_file_path =  data_file_path
        self.expenses = []
        self.load_expenses()

    def load_expenses(self):
        """Load expenses from the JSON file if it exists.

        If the file does not exist or contains invalid JSON, start with an empty list.
        """
        if not os.path.exists(self.data_file_path):
            self.expenses = []
            return

        with open(self.data_file_path, "r") as file:
            try:
                self.expenses = json.load(file)
            except json.JSONDecodeError:
                self.expenses = []

    def save_expenses(self):
        """Save all current expenses to the JSON file."""
        with open(self.data_file_path, "w") as file:
            json.dump(self.expenses, file, indent=4)

    def has_expenses(self) -> bool:
        """Return True when expenses exist, otherwise print a message and return False."""
        if not self.expenses:
            print("No expneses found.")
            return False
        return True
    
    def sort_expenses_by_date(self):
        """Sort expenses in ascending order by date."""
        self.expenses.sort(
            key=lambda expense: datetime.strptime(expense["date"], "%Y-%m-%d")
        )

    def create_expense_record(self) -> dict:
        """Collect user input and build one expense record."""
        return {
            "amount": get_amount(),
            "category": get_category(),
            "description": get_description(),
            "date": get_date(),
        }

    def add_expense(self):
        """Prompt the user for expense details, then save the new expense."""
        expense_record = self.create_expense_record()
        self.expenses.append(expense_record)
        self.save_expenses()
        print("Expense added successfully!")

    def display_expenses(self):
        """Print all expenses in a numbered list after sorting by date."""
        self.sort_expenses_by_date()

        if not self.has_expenses():
            return

        for index, expense in enumerate(self.expenses, start=1):
            print(f"{index}. Amount: ${expense['amount']}")
            print(f"   Category: {expense['category']}")
            print(f"   Description: {expense['description']}")
            print(f"   Date: {expense['date']}")
            print()

    def get_valid_index(self, prompt_message: str):
        """Ask the user for an expense number and return a valid list index.

        Returns None when the input is not a valid selection.
        """
        if not self.has_expenses():
            return None

        selection = input(prompt_message).strip()
        if not selection.isdigit():
            print("Invalid number.")
            return None

        expense_index = int(selection) - 1
        if 0 <= expense_index < len(self.expenses):
            return expense_index

        print("Invalid selection.")
        return None

    def delete_expense(self):
            """Display expenses, delete the selected one, and save the updated list."""
            self.display_expenses()
            expense_index = self.get_valid_index("Enter the expense number to delete: ")

            if expense_index is None:
                return

            self.expenses.pop(expense_index)
            self.save_expenses()
            print("Expense deleted successfully.")

    def update_expense(self, expense_index: int):
        """Replace an existing expense with newly entered values."""
        updated_expense = self.create_expense_record()
        self.expenses[expense_index] = updated_expense
        self.save_expenses()
        print("Expense updated successfully!")

    def edit_expense(self):
        """Display expenses, prompt for one to edit, then save changes."""
        self.display_expenses()
        expense_index = self.get_valid_index("Enter the expense number to edit: ")

        if expense_index is None:
            return

        self.update_expense(expense_index)

    def view_total_spending(self):
        """Calculate and display the sum of all expense amounts."""
        if not self.has_expenses():
            return
        
         # sum(...) is a clean Python pattern for accumulating numeric values.
        total_spending = sum(float(expense.get("amount", 0)) for expense in self.expenses)
        print(f"Total spending: ${total_spending}")

    def calculate_category_totals(self, expenses=None) -> dict:
        """Return a dictionary mapping each category to its total spending."""
        expenses = expenses if expenses is not None else self.expenses
        category_totals = {}

        # This loop groups amounts by category.
        for expense in expenses:
            category_name = expense["category"]
            amount = float(expense["amount"])
            category_totals[category_name] = category_totals.get(category_name, 0) + amount

        return category_totals

    def view_spending_by_category(self):
        """Display total spending for each category."""
        if not self.has_expenses():
            return
        
        category_totals = self.calculate_category_totals()

        print("\nSpending by Category:")
        for category_name, total_amount in category_totals.items():
            print(f"{category_name}: ${total_amount}")

    def view_highest_expense(self):
        """Display the expense with the highest amount."""
        if not self.has_expenses():
            return

        highest_expense = max(self.expenses, key=lambda expense: float(expense["amount"]))
        print("\nHighest Expense: ")
        print(
            f"${highest_expense['amount']} - {highest_expense['category']} - {highest_expense['date']}"
            )

    def view_lowest_expense(self):
        """Display the expense with the lowest amount."""
        if not self.has_expenses():
            return

        lowest_expense = min(self.expenses, key=lambda expense: float(expense["amount"]))
        print("\nLowest Expense:")
        print(
            f"${lowest_expense['amount']} - {lowest_expense['category']} - {lowest_expense['date']}"
            )

    def get_expenses_for_month(self, target_month: str):
        """Return expenses whose date starts with the given YYYY-MM string."""
        return [expense for expense in self.expenses if expense["date"].startswith(target_month)]


    def monthly_spending_summary(self):
        """Display total and category totals for a selected month."""
        if not self.has_expenses():
            return

        target_month = input("Enter moth (YYYY-MM): ").strip()
        monthly_expenses = self.get_expenses_for_month(target_month)

        if not monthly_expenses:
            print(f"No expenses found for {target_month}.")
            return
        
        monthly_total = sum(float(expense['amount']) for expense in monthly_expenses)
        category_totals = self.calculate_category_totals(monthly_expenses)
        
        print(f"\nTotal spending: for {target_month}: ${monthly_total}")
        print("\nSpending by category:")
        for category_name, amount in category_totals.items():
            print(f"{category_name}: ${amount}")

# ---- Input helpers ----
def get_non_empty_input(prompt_message: str) -> str:
    """Keep prompting until the user enters non-empty text."""
    while True:
        user_input = input(prompt_message).strip()
        if user_input:
            return user_input
        print("Input cannot be empty.")

def get_amount() -> float:
    """Prompt for a valid numeric amount and return it as a float."""
    while True:
        amount_text = get_non_empty_input("Enter amount: ")
        if amount_text.replace(".", "", 1).isdigit():
            return float(amount_text)
        print("Invalid amount. Please enter a number.")

def get_category() -> str:
    """Prompt for an expense category."""
    return get_non_empty_input("Enter category: ")

def get_description() -> str:
    """Prompt for an expense description."""
    return get_non_empty_input("Enter description: ")

def get_date() -> str:
    """Prompt for a valid date and return it in YYYY-MM-DD format."""
    while True:
        print("Enter date:")
        day_text = get_non_empty_input("Day: ")
        month_text = get_non_empty_input("Month: ")
        year_text = get_non_empty_input("Year: ")

        if not (day_text.isdigit() and month_text.isdigit() and year_text.isdigit()):
            print("Date values must be numbers.")
            continue
        
        current_year = datetime.now().year
        if not (2000 <= int(year_text) <= current_year):
            print(f"Year must be between 2000 and {current_year}.")
            continue

        try:
            valid_date = datetime(int(year_text), int(month_text), int(day_text))
            date = valid_date.strftime("%Y-%m-%d")
            return date
        except ValueError:
            print("Invalid date. Please enter a real calendar date.")

def print_menu():
    """Display the main menu."""
    print("\nExpense Tracker Menu")
    print("1. Add an expense")
    print("2. View all expenses")
    print("3. View total spending")
    print("4. View spending by category")
    print("5. View highest and lowest expenses")
    print("6. Delete an expense")
    print("7. Edit an expense")
    print("8. View monthly spending summary")
    print("Q. Quit")

def main():
    """Run the menu-driven expense tracker application."""
    tracker = ExpenseTracker("expense.json")

    while True:
        print_menu()
        choice = input("Select an option: ").strip().lower()

        match choice:
            case "1":
                tracker.add_expense()
            
            case "2":
                tracker.display_expenses()
            
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