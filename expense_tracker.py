"""
Smart Expense Tracker Application
----------------------------------
Covers only: Control Structures & Arrays, OOP, NumPy, Pandas, Matplotlib & Seaborn
(as per the project brief)
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


VALID_CATEGORIES = ["Food", "Transport", "Utilities", "Entertainment", "Shopping", "Health", "Other"]


class ExpenseTracker:
    """Logs, analyzes, filters, and reports on personal expenses."""

    def __init__(self, csv_file="expenses.csv"):
        self.csv_file = csv_file
        self.columns = ["Date", "Amount", "Category", "Description"]

        # Load existing dataset if present, otherwise start empty
        if os.path.exists(self.csv_file):
            self.df = pd.read_csv(self.csv_file)
            self.df["Date"] = pd.to_datetime(self.df["Date"], errors="coerce")
            self.df["Amount"] = pd.to_numeric(self.df["Amount"], errors="coerce")
            # Handle missing / invalid rows
            self.df.dropna(subset=["Date", "Amount"], inplace=True)
        else:
            self.df = pd.DataFrame(columns=self.columns)

    # ---------------- 1. Expense Input & Validation (Control Structures) ----------------
    def add_expense(self, date, amount, category, description):
        """Validate inputs with control structures, then log a new expense."""

        if amount <= 0:
            print(f"[Rejected] Amount must be positive. Got: {amount}")
            return False

        if category not in VALID_CATEGORIES:
            print(f"[Rejected] Invalid category '{category}'. Choose from {VALID_CATEGORIES}")
            return False

        try:
            parsed_date = pd.to_datetime(date)
        except Exception:
            print(f"[Rejected] Invalid date format '{date}'. Use YYYY-MM-DD.")
            return False

        new_row = {
            "Date": parsed_date,
            "Amount": amount,
            "Category": category,
            "Description": description
        }
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        print(f"[Added] {date} | {amount} | {category} | {description}")
        return True

    def save(self):
        """Persist current data back to the CSV file."""
        self.df.to_csv(self.csv_file, index=False)
        print(f"Data saved to {self.csv_file}")

    # ---------------- 2 & 3. Analysis & Computations (NumPy + Pandas) ----------------
    def get_summary(self):
        """Return total, average, max, min and category-wise expense breakdown."""
        if self.df.empty:
            print("No expense data available.")
            return None

        amounts = self.df["Amount"].to_numpy()  # NumPy array for numeric computation

        total = np.sum(amounts)
        average = np.mean(amounts)
        maximum = np.max(amounts)
        minimum = np.min(amounts)

        category_totals = self.df.groupby("Category")["Amount"].sum()
        top_category = category_totals.idxmax()

        summary = {
            "total_expense": total,
            "average_expense": average,
            "max_expense": maximum,
            "min_expense": minimum,
            "category_totals": category_totals,
            "top_category": top_category
        }

        print("\n----- Expense Summary -----")
        print(f"Total Expense   : {total:.2f}")
        print(f"Average Expense : {average:.2f}")
        print(f"Highest Expense : {maximum:.2f}")
        print(f"Lowest Expense  : {minimum:.2f}")
        print(f"Top Category    : {top_category}")
        print("\nCategory-wise Totals:")
        print(category_totals)

        return summary

    # ---------------- Filtering (Pandas) - Better Filtering ----------------
    def filter_expenses(self, category=None, start_date=None, end_date=None,
                         min_amount=None, max_amount=None, keyword=None,
                         sort_by=None, ascending=True):
        """Filter expenses by category, date range, amount range, and/or a
        keyword in the description. Optionally sort the results."""
        filtered = self.df.copy()

        if category is not None:
            filtered = filtered[filtered["Category"] == category]

        if start_date is not None:
            filtered = filtered[filtered["Date"] >= pd.to_datetime(start_date)]

        if end_date is not None:
            filtered = filtered[filtered["Date"] <= pd.to_datetime(end_date)]

        if min_amount is not None:
            filtered = filtered[filtered["Amount"] >= min_amount]

        if max_amount is not None:
            filtered = filtered[filtered["Amount"] <= max_amount]

        if keyword is not None:
            filtered = filtered[filtered["Description"].str.contains(keyword, case=False, na=False)]

        if sort_by is not None and sort_by in filtered.columns:
            filtered = filtered.sort_values(by=sort_by, ascending=ascending)

        print(f"\nFiltered results: {len(filtered)} record(s) found.")
        if not filtered.empty:
            print(f"Filtered Total : {filtered['Amount'].sum():.2f}")
            print(f"Filtered Average: {filtered['Amount'].mean():.2f}")
        print(filtered)
        return filtered

    # ---------------- Report Generation ----------------
    def generate_report(self):
        """Output a summary report with key derived metrics."""
        summary = self.get_summary()
        if summary is None:
            return None

        monthly = self.df.copy()
        monthly["Month"] = monthly["Date"].dt.to_period("M")
        monthly_avg = monthly.groupby("Month")["Amount"].mean()
        monthly_total = monthly.groupby("Month")["Amount"].sum()          # Monthly total
        top_month = monthly_total.idxmax()                                # Top spending month

        daily_total = self.df.groupby("Date")["Amount"].sum()
        top_day = daily_total.idxmax()                                    # Top spending day

        category_pct = (summary["category_totals"] / summary["total_expense"]) * 100

        # Small report improvements: transaction count + single highest expense record
        total_transactions = len(self.df)
        top_expense_row = self.df.loc[self.df["Amount"].idxmax()]

        print("\n----- Detailed Report -----")
        print(f"\nTotal Transactions: {total_transactions}")
        print("\nMonthly Total Spending:")
        print(monthly_total)
        print(f"\nTop Spending Month: {top_month}  (Total: {monthly_total.loc[top_month]:.2f})")
        print("\nMonthly Average Spending:")
        print(monthly_avg)
        print(f"\nTop Spending Day: {top_day.date()}  (Total: {daily_total.loc[top_day]:.2f})")
        print("\nSpending Percentage by Category:")
        print(category_pct.round(2))
        print("\nSingle Highest Expense Record:")
        print(top_expense_row)

        return {
            "monthly_total": monthly_total,
            "monthly_average": monthly_avg,
            "top_month": top_month,
            "top_day": top_day,
            "category_percentage": category_pct,
            "total_transactions": total_transactions,
            "top_expense_row": top_expense_row
        }

    # ---------------- 4. Data Visualization (Matplotlib & Seaborn) ----------------
    def visualize(self, display=False):
        """Generate bar chart, line graph, pie chart, and histogram.
        If display=True, each chart is also shown on screen (Graph Display)."""
        if self.df.empty:
            print("No data to visualize.")
            return

        sns.set_theme(style="whitegrid")

        # Bar Chart: Total expenses by category
        category_totals = self.df.groupby("Category")["Amount"].sum()
        plt.figure(figsize=(8, 5))
        sns.barplot(x=category_totals.index, y=category_totals.values, palette="viridis")
        plt.title("Total Expenses by Category")
        plt.xlabel("Category")
        plt.ylabel("Total Amount")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.savefig("bar_chart_category.png")
        if display:
            plt.show()
        plt.close()

        # Line Graph: Spending trend over time
        daily_totals = self.df.groupby("Date")["Amount"].sum().sort_index()
        plt.figure(figsize=(8, 5))
        plt.plot(daily_totals.index, daily_totals.values, marker="o", color="teal")
        plt.title("Spending Trend Over Time")
        plt.xlabel("Date")
        plt.ylabel("Total Amount Spent")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.savefig("line_chart_trend.png")
        if display:
            plt.show()
        plt.close()

        # Pie Chart: Proportional spending distribution by category
        plt.figure(figsize=(6, 6))
        plt.pie(category_totals.values, labels=category_totals.index, autopct="%1.1f%%", startangle=90)
        plt.title("Spending Distribution by Category")
        plt.tight_layout()
        plt.savefig("pie_chart_distribution.png")
        if display:
            plt.show()
        plt.close()

        # Histogram: Frequency of expense amounts
        plt.figure(figsize=(8, 5))
        sns.histplot(self.df["Amount"], bins=10, kde=True, color="orange")
        plt.title("Frequency of Expense Amounts")
        plt.xlabel("Expense Amount")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig("histogram_amounts.png")
        if display:
            plt.show()
        plt.close()

        print("\nVisualizations saved: bar_chart_category.png, line_chart_trend.png, "
              "pie_chart_distribution.png, histogram_amounts.png")


def main_menu():
    tracker = ExpenseTracker("expenses.csv")

    while True:
        print("\n===== Smart Expense Tracker =====")
        print(" 1. Add Expense")
        print(" 2. View All Expenses")
        print(" 3. View Summary")
        print(" 4. Filter Expenses")
        print(" 5. Generate Report")
        print(" 6. Visualize Data")
        print(" 7. Save & Exit")
        print("-----------------------------------")

        choice = input("Enter your choice (1-7): ").strip()

        match choice:
            case "1":
                date = input("Date (YYYY-MM-DD): ").strip()
                try:
                    amount = float(input("Amount: ").strip())
                except ValueError:
                    print("Amount must be a number.")
                    continue
                category = input(f"Category {VALID_CATEGORIES}: ").strip()
                description = input("Description: ").strip()
                tracker.add_expense(date, amount, category, description)

            case "2":
                if tracker.df.empty:
                    print("No expenses recorded yet.")
                else:
                    print(f"\nAll Expenses ({len(tracker.df)} records):")
                    print(tracker.df.sort_values(by="Date"))

            case "3":
                tracker.get_summary()

            case "4":
                print("\n--- Filter Expenses (leave any field blank to skip) ---")
                category = input("Category: ").strip() or None
                start_date = input("Start date (YYYY-MM-DD): ").strip() or None
                end_date = input("End date (YYYY-MM-DD): ").strip() or None
                min_amount_in = input("Minimum amount: ").strip()
                max_amount_in = input("Maximum amount: ").strip()
                keyword = input("Keyword in description: ").strip() or None
                sort_by = input("Sort by (Date/Amount/Category, blank to skip): ").strip() or None
                order = input("Sort order (asc/desc, default asc): ").strip().lower()

                min_amount = float(min_amount_in) if min_amount_in else None
                max_amount = float(max_amount_in) if max_amount_in else None
                ascending = order != "desc"

                tracker.filter_expenses(category=category, start_date=start_date, end_date=end_date,
                                         min_amount=min_amount, max_amount=max_amount,
                                         keyword=keyword, sort_by=sort_by, ascending=ascending)

            case "5":
                tracker.generate_report()

            case "6":
                show_choice = input("Display graphs on screen as well as saving them? (y/n): ").strip().lower()
                tracker.visualize(display=(show_choice == "y"))

            case "7":
                tracker.save()
                print("Goodbye!")
                break

            case _:
                print("Invalid choice. Please select between 1 and 7.")


if __name__ == "__main__":
    main_menu()