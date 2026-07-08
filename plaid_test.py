from services.plaid import (
    create_link_token,
    sandbox_create_public_token,
    exchange_public_token,
    sync_transactions,
    sync_transactions_with_retry
)

TEST_USER_ID = "test-user-123"

# create a link token
print("Creating link token...")
link_token = create_link_token(TEST_USER_ID)
print(f"  link_token: {link_token[:30]}...")

# simulate a user completing Plaid Link
print("\nGenerating fake public token (Sandbox shortcut)...")
public_token = sandbox_create_public_token()
print(f"  public_token: {public_token[:30]}...")

# exchange it for an access token
print("\nExchanging public token for access token...")
access_token, item_id = exchange_public_token(public_token)
print(f"  access_token: {access_token[:20]}...")
print(f"  item_id: {item_id}")

# sync transactions
print("\nSyncing transactions...")
result = sync_transactions_with_retry(access_token, cursor=None)
print(f"  Added: {len(result['added'])} transactions")
print(f"  Has more: {result['has_more']}")

if result['added']:
    print("\n  Sample transaction (already mapped to your category system):")
    sample = result['added'][0]
    for key, value in sample.items():
        print(f"    {key}: {value}")

print("\nAll steps completed.")