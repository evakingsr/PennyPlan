import time
from database import (
    create_user_admin,
    login_user,
    get_user_id,
    add_expense,
    get_expenses,
    save_plaid_credentials,
)
from services.plaid import (
    create_link_token,
    sandbox_create_public_token,
    exchange_public_token,
    sync_transactions,
)
from services.aggregator import aggregate_spending
from services.gemini import generate_report

EMAIL = "pennyplan.demo.user@gmail.com"
PASSWORD = "DemoPassword123!"
NAME = "Demo User"


def sync_with_retry(access_token, cursor=None, max_attempts=5):
    for attempt in range(max_attempts):
        result = sync_transactions(access_token, cursor)
        if result['added'] or result['modified']:
            return result
        print(f"  No transactions yet, retrying... ({attempt + 1}/{max_attempts})")
        time.sleep(2)
    return result


print("Creating demo user...")
try:
    signup_response = create_user_admin(EMAIL, PASSWORD, NAME)
    user_id = signup_response.user.id
    print(f"  Created. user_id: {user_id}")
except Exception as e:
    print(f"  Signup failed (may already exist): {e}")
    print("  Attempting login instead...")
    login_response = login_user(EMAIL, PASSWORD)
    user_id = get_user_id(login_response)
    print(f"  Logged in. user_id: {user_id}")

print("\nTesting real login flow...")
login_response = login_user(EMAIL, PASSWORD)
confirmed_user_id = get_user_id(login_response)
print(f"  Login successful. user_id: {confirmed_user_id}")

print("\nCreating link token...")
link_token = create_link_token(user_id)
print(f"  link_token: {link_token[:30]}...")

print("\nSimulating Plaid Link success...")
public_token = sandbox_create_public_token()
print(f"  public_token: {public_token[:30]}...")

print("\nExchanging for access token...")
access_token, item_id = exchange_public_token(public_token)
print(f"  access_token: {access_token[:20]}...")

print("\nSaving Plaid credentials to Supabase...")
save_plaid_credentials(user_id, access_token, item_id)
print("  Saved.")

print("\nSyncing transactions...")
result = sync_with_retry(access_token)
print(f"  Added: {len(result['added'])} transactions")

save_plaid_credentials(user_id, access_token, item_id, plaid_cursor=result['next_cursor'])

print("\nSaving transactions to Supabase...")
for txn in result['added']:
    add_expense(
        user_id=user_id,
        category=txn['category'],
        description=txn['description'],
        amount=txn['amount'],
        expense_date=txn['expense_date'],
        source=txn['source'],
        plaid_transaction_id=txn['plaid_transaction_id'],
    )
print(f"  Saved {len(result['added'])} expenses.")

print("\nReading back all expenses and generating report...")
all_expenses = get_expenses(user_id)
print(f"  Total expenses in Supabase: {len(all_expenses)}")

this_month = aggregate_spending(all_expenses, period='this_month')
last_month = aggregate_spending(all_expenses, period='last_month')
report = generate_report(this_month, last_month)

print(f"\n  Summary: {report['summary']}")
print(f"  Trends: {report['trends']}")
print(f"  Tips: {report['tips']}")

print(f"\nDemo user ready. Email: {EMAIL} / Password: {PASSWORD}")
print(f"user_id: {user_id}")
print("\nAll steps completed.")