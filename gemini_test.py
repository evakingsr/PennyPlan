from datetime import date, timedelta
from services.gemini import generate_report, categorize_manual_entry
from services.aggregator import aggregate_spending

today = date.today()
last_month_date = (today.replace(day=1) - timedelta(days=15)).isoformat()

fake_expenses = [
    {"category": "Rent", "amount": 1200.00, "expense_date": today.isoformat()},
    {"category": "Groceries", "amount": 84.20, "expense_date": today.isoformat()},
    {"category": "Dining", "amount": 11.75, "expense_date": today.isoformat()},
    {"category": "Subscriptions", "amount": 15.99, "expense_date": today.isoformat()},
    {"category": "Rent", "amount": 1200.00, "expense_date": last_month_date},
    {"category": "Groceries", "amount": 60.00, "expense_date": last_month_date},
    {"category": "Dining", "amount": 40.00, "expense_date": last_month_date},
]

print("Testing categorize_manual_entry()...\n")
manual_entries = [
    ("coffee at Blue Bottle", 6.50),
    ("Uber ride downtown", 22.00),
    ("bought a birthday gift", 40.00),
]
for description, amount in manual_entries:
    category = categorize_manual_entry(description, amount)
    print(f"  {description:30s} ${amount:>8.2f}  ->  {category}")

print("\nTesting aggregate_spending()...\n")
this_month = aggregate_spending(fake_expenses, period='this_month')
last_month = aggregate_spending(fake_expenses, period='last_month')
print(f"  This month: {this_month}")
print(f"  Last month: {last_month}")

print("\nTesting generate_report()...\n")
report = generate_report(this_month, last_month)
print(f"  Summary: {report['summary']}")
print(f"  Trends: {report['trends']}")
print(f"  Tips: {report['tips']}")

print("\nAll steps completed.")