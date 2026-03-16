import os
import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self, file_name):
        self.file_name =  file_name
        self.expenses = []
        self.load_expenses()

    def load_expenses(self):
        if not os.path.exists(self.file_name):
            return []

        with open(self.file_name, "r") as f:
            try:
                self.expenses = json.load(f)
            except json.JSONDecodeError:
                self.expenses = []

    def sort_expenses_by_date(self):
        self.expenses.sort(
            key=lambda exp: datetime.strptime(exp["date"], "%Y-%m-%d")
        )

    def save_expenses(self):
        with open(self.file_name, "w") as f:
            json.dump(self.expenses, f, indent=4)

    def check_is_there_expense(self):
        if not self.expenses:
            print("No expneses found.")
            return False
        return True

    def add_expense(self):
        new_expense_list = {
            "amount": get_amount(),
            "category": get_category(),
            "description": get_description(),
            "date": get_date()
        }

        self.expenses.append(new_expense_list)
        self.save_expenses()
        print("Expense added!")

    def view_expense(self):
        self.sort_expenses_by_date()

        if not self.check_is_there_expense():
            return

        for i, exp in enumerate(self.expenses, start=1):
            print(f"{i}. Amount: ${exp['amount']}")
            print(f"   Category: {exp['category']}")
            print(f"   Description: {exp['description']}")
            print(f"   Date: {exp['date']}")
            print()

    def delete_expense(self):
        self.view_expense()

        choice = input("Enter number to delete: ")

        if not choice.isdigit():
            print("Invalid number")
            return

        index = int(choice) - 1

        if 0 <= index < len(self.expenses):
            self.expenses.pop(index)
            self.save_expenses()
            print("Deleted!")
        else:
            print("Invalid choice")

    def view_total_spending(self):
        if not self.check_is_there_expense():
            return
        
        total = 0

        for exp in self.expenses:
            total += float(exp.get("amount", 0))
        print(f"Total spending: {total}$")

    def view_spending_by_category(self):
        if not self.check_is_there_expense():
            return
        
        category_total = {}

        for exp in self.expenses:
            category = exp['category']
            amount = float(exp['amount'])

            if category in category_total:
                category_total[category] += amount
            else:
                category_total[category] = amount

        print("\nSpending by Category:")
        for cate, total in category_total.items():
            print(f"{cate}: ${total}")

    def view_highest_expense(self):
        self.check_is_there_expense()

        highest = max(self.expenses, key=lambda exp: float(exp["amount"]))

        print("\nHighest Expense: ")
        print(f"${highest['amount']} - {highest['category']} - {highest['date']}")

    def view_lowest_expense(self):
        self.check_is_there_expense()

        lowest = min(self.expenses, key=lambda exp: float(exp["amount"]))

        print("\nLowest Expense:")
        print(f"${lowest['amount']} - {lowest['category']} - {lowest['date']}")

    def edit_expense(self):
        self.view_expense()
        
        index = int(input("Enter a number: ")) - 1

        if 0 <= index < len(self.expenses):

            new_amount = get_amount()
            new_category = get_category()
            new_description = get_description()
            new_date = get_date()

            self.expenses[index]["amount"] = new_amount
            self.expenses[index]["category"] = new_category
            self.expenses[index]["description"] = new_description
            self.expenses[index]["date"] = new_date

            print("Expense update!")
            self.save_expenses()

        else:
            print("Invalid number")

    def monthly_spending_summary(self):
        self.check_is_there_expense()

        month = input("Enter month (YYYY-MM): ")

        total =  0
        categories = {}

        for expense in self.expenses:

            if expense["date"].startswith(month):

                total += expense["amount"]

                category = expense["category"]

                if category in categories:
                    categories[category] += expense["amount"]
                else:
                    categories[category] = expense["amount"]

        print(f"\nTotal spending: ${total}")

        print("\nBy category:")
        for category, amount in categories.items():
            print(category, ":", amount)

# ---- amount ----
def get_amount():
    while True:
        amount = get_non_empty_input("Enter amount: ")
        if amount.replace(".", "", 1).isdigit():
            return float(amount)
        print("Invalid amount! Please enter a number.")

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
        day = get_non_empty_input("Date: ")
        month = get_non_empty_input("Month: ")
        year = get_non_empty_input("Year: ")

        if not (day.isdigit() and month.isdigit() and year.isdigit()):
            print("Date must be number!")
            continue

        if not (2000 <= int(year) <= 2026):
            print("Year must be between 2000 and 2026")
            continue

        try:
            valid_date = datetime(int(year), int(month), int(day))
            date = valid_date.strftime("%Y-%m-%d")
            return date

        except ValueError:
            print("Invalid date! Please enter a real calendar date.")

def get_non_empty_input(message):
    while True:
        value = input(message).strip()
        if value:
            return value
        print("Input cannot be empty.")

def main():
    tracker = ExpenseTracker("expense.json")

    while True:
        print("1. Add expenses.")
        print("2. View expenses.")
        print("3. View total spending.")
        print("4. View spending by category.")
        print("5. View highest expense and lowest expense.")
        print("6. To remove expense.")
        print("7. edit expense feature.")
        print("8. monthly spending summary.")
        print("q. Quit")

        choice = input(": ").lower()

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
                tracker.view_highest_expense
                tracker.view_lowest_expense
            
            case "6":
                tracker.delete_expense()
            
            case "7":
                tracker.edit_expense()
            
            case "8":
                tracker.monthly_spending_summary()
            
            case "q" | "quit" | "exit":
                print("Bye")
                break

            case _:
                print("Invalid choice")


if "__main__" == __name__:
    main()