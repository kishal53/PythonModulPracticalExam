# Smart Expense Tracker Application

A Python-based expense tracker that lets you log, analyze, filter, and visualize
personal spending. Built using **Control Structures, OOP, NumPy, Pandas, Matplotlib,
and Seaborn**, as required by the project brief.

## Features

1. **Expense Input & Validation** — logs a new expense after validating that the
   amount is positive, the category is valid, and the date is well-formed.
2. **Expense Tracker Class (OOP)** — an `ExpenseTracker` class with:
   - `add_expense()` — logs new expenses
   - `get_summary()` — total, average, highest, lowest expense, and category totals
   - `filter_expenses()` — filter by category, date range, amount range, or
     keyword, with sorting support
   - `generate_report()` — monthly totals/averages, top spending month, top
     spending day, category percentage breakdown, transaction count, and the
     single highest expense
3. **Analysis & Computations** — NumPy for numeric calculations (sum, mean, max,
   min); Pandas for loading, cleaning, grouping, and filtering the data.
4. **Data Visualization** — Matplotlib & Seaborn charts:
   - Bar chart — total expenses by category
   - Line graph — spending trend over time
   - Pie chart — proportional spending distribution by category
   - Histogram — frequency of expense amounts

## Requirements

- Python 3.8+
- Packages: `numpy`, `pandas`, `matplotlib`, `seaborn`

Install dependencies:

```bash
pip install numpy pandas matplotlib seaborn
```

## Setup Instructions

1. Place `expense_tracker.py` and your `expenses.csv` dataset in the same folder.
2. `expenses.csv` must have these columns:

   | Date       | Amount | Category      | Description       |
   |------------|--------|---------------|--------------------|
   | 2026-07-01 | 250.00 | Food          | Lunch with friends |
   | 2026-07-02 | 500.00 | Transport     | Fuel               |

3. Run the script:

   ```bash
   python expense_tracker.py
   ```

   If `expenses.csv` doesn't exist yet, the app starts with an empty dataset and
   creates the file once you save.

## Using the App

On launch you'll see a menu:

```
===== Smart Expense Tracker =====
 1. Add Expense
 2. View All Expenses
 3. View Summary
 4. Filter Expenses
 5. Generate Report
 6. Visualize Data
 7. Save & Exit
```

- **Add Expense** — enter date, amount, category, and description; invalid
  entries are rejected with a clear message.
- **View All Expenses** — lists every recorded expense, sorted by date.
- **View Summary** — total, average, highest, lowest, and category-wise totals.
- **Filter Expenses** — filter by category, date range, min/max amount, or a
  keyword in the description, and optionally sort the results.
- **Generate Report** — adds monthly totals, top spending month, top spending
  day, category spending percentages, transaction count, and the single
  highest expense.
- **Visualize Data** — saves the bar chart, line graph, pie chart, and
  histogram as PNG files; optionally displays them on screen too.
- **Save & Exit** — writes all changes back to `expenses.csv`.

## Output Files

Running "Visualize Data" produces:

- `bar_chart_category.png`
- `line_chart_trend.png`
- `pie_chart_distribution.png`
- `histogram_amounts.png`

## Notes

- All amounts must be positive numbers; invalid rows are skipped when loading.
- Dates should be in `YYYY-MM-DD` format.
- Categories are limited to: `Food, Transport, Utilities, Entertainment,
  Shopping, Health, Other`.
