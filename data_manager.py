import pandas as pd
import csv
import os
from collections import defaultdict

EXPENSE_FILE = 'expenses.csv'

def get_expenses():
    """Reads and returns all expenses from the CSV file."""
    try:
        with open(EXPENSE_FILE, 'r') as f:
            reader = csv.reader(f)
            expenses = list(reader)
            if len(expenses) > 1:
                return expenses[1:]
            else:
                return []
    except FileNotFoundError:
        return []

def add_expense_to_csv(date, amount, category, payment_method):
    """Adds a new expense to the CSV file."""
    try:
        with open(EXPENSE_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(['Date', 'Amount', 'Category', 'Payment Method'])
            writer.writerow([date, amount, category, payment_method])
        return True
    except IOError:
        return False

def generate_report_data():
    """Calculates and returns total spending per category."""
    expenses = get_expenses()
    spending_by_category = defaultdict(float)
    for row in expenses:
        try:
            category = row[2].strip().title()
            amount = float(row[1])
            spending_by_category[category] += amount
        except (ValueError, IndexError):
            continue
    return sorted(spending_by_category.items())

def get_dataframe():
    """Reads expense data into a pandas DataFrame."""
    # Check if the file exists and is not empty
    if not os.path.exists(EXPENSE_FILE) or os.path.getsize(EXPENSE_FILE) == 0:
        return pd.DataFrame(columns=['Date', 'Amount', 'Category', 'Payment Method'])
    
    df = pd.read_csv(EXPENSE_FILE)
    
    # Check if the DataFrame is empty before trying to access columns
    if not df.empty:
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        df['Date'] = pd.to_datetime(df['Date'])
    
    return df

def delete_expense(df, index):
    """Deletes an expense from the DataFrame and saves the updated data."""
    if index is not None and not df.empty and index < len(df):
        df = df.drop(index).reset_index(drop=True)
        df.to_csv(EXPENSE_FILE, index=False)
        return True
    return False