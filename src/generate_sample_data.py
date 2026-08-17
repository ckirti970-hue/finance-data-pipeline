import random
import pandas as pd
from datetime import datetime, timedelta

random.seed(42)

VENDORS = ["Reliance Traders", "Sunrise Electricals", "Kirti Enterprises",
           "Bharat Supplies", "Om Distributors", "Shree Hardware", "Metro Logistics"]

CATEGORIES_MESSY = ["sales", "Sales", "SALES", "purchase", "Purchase",
                     "utilities", "Utilties", "rent", "Rent", "salary", "Salary "]

DATE_FORMATS = ["%d-%m-%Y", "%Y/%m/%d", "%d/%m/%Y", "%b %d, %Y"]


def random_date(start_days_ago=180, end_days_ago=0):
    days = random.randint(end_days_ago, start_days_ago)
    return datetime.now() - timedelta(days=days)


def messy_date_str(dt):
    fmt = random.choice(DATE_FORMATS)
    return dt.strftime(fmt)


def messy_amount():
    amount = round(random.uniform(500, 85000), 2)
    style = random.choice(["plain", "rupee_symbol", "comma", "negative_paren"])
    if style == "plain":
        return str(amount)
    if style == "rupee_symbol":
        return f"₹{amount:,.2f}"
    if style == "comma":
        return f"{amount:,.2f}"
    if style == "negative_paren":
        return f"({amount:,.2f})"
    return str(amount)


def generate_bank_transactions(n=120):
    rows = []
    for i in range(n):
        dt = random_date()
        row = {
            "Txn Date": messy_date_str(dt),
            "Description": f"{random.choice(VENDORS)} PYMT REF{random.randint(1000,9999)}",
            "Amount (INR)": messy_amount(),
            "Type": random.choice(["CR", "DR"]),
            "Category": random.choice(CATEGORIES_MESSY + ["", None]),
        }
        rows.append(row)

    for _ in range(6):
        rows.append(random.choice(rows[:n]).copy())

    df = pd.DataFrame(rows)
    df.to_csv("data/raw/bank_transactions.csv", index=False)
    print(f"Created bank_transactions.csv ({len(df)} rows)")


def generate_invoices(n=60):
    rows = []
    for i in range(n):
        dt = random_date(150, 0)
        rows.append({
            "InvoiceNo": f"INV-{1000+i}",
            "Client": random.choice(VENDORS),
            "InvoiceDate": messy_date_str(dt),
            "Total Amount": messy_amount(),
            "Status": random.choice(["Paid", "paid", "PAID", "Pending", "pending", None]),
        })
    df = pd.DataFrame(rows)
    df.loc[df.sample(frac=0.05, random_state=1).index, "Total Amount"] = None
    df.to_excel("data/raw/invoices.xlsx", index=False)
    print(f"Created invoices.xlsx ({len(df)} rows)")


def generate_expenses(n=80):
    rows = []
    for i in range(n):
        dt = random_date(150, 0)
        rows.append({
            "date": dt.strftime("%d/%m/%Y"),
            "vendor_name": random.choice(VENDORS),
            "expense_category": random.choice(CATEGORIES_MESSY),
            "amount_inr": messy_amount(),
            "notes": random.choice(["", "urgent", "recurring", "one-time", None]),
        })
    df = pd.DataFrame(rows)
    df.to_csv("data/raw/expenses.csv", index=False)
    print(f"Created expenses.csv ({len(df)} rows)")


if __name__ == "__main__":
    generate_bank_transactions()
    generate_invoices()
    generate_expenses()
    print("\nSample messy data generated in data/raw/")


