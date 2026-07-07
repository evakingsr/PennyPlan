import os
import plaid
from plaid.api import plaid_api
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from dotenv import load_dotenv

load_dotenv()

_client = None

def get_client():
    global _client
    if _client is None:
        env = os.environ.get('PLAID_ENV', 'sandbox')
        host = plaid.Environment.Sandbox if env == 'sandbox' else plaid.Environment.Production
        configuration = plaid.Configuration(
            host=host,
            api_key={
                'clientId': os.environ['PLAID_CLIENT_ID'],
                'secret': os.environ['PLAID_SECRET'],
            }
        )
        _client = plaid_api.PlaidApi(plaid.ApiClient(configuration))
    return _client


def create_link_token(user_id: str) -> str:
    client = get_client()
    request = LinkTokenCreateRequest(
        products=[Products('transactions')],
        client_name="PennyPlan",
        country_codes=[CountryCode('US')],
        language='en',
        user=LinkTokenCreateRequestUser(client_user_id=user_id)
    )
    response = client.link_token_create(request)
    return response['link_token']


def exchange_public_token(public_token: str) -> tuple:
    """Returns (access_token, item_id) — save both to the user's profile."""
    client = get_client()
    response = client.item_public_token_exchange(
        ItemPublicTokenExchangeRequest(public_token=public_token)
    )
    return response['access_token'], response['item_id']


def sync_transactions(access_token: str, cursor: str | None = None) -> dict:
    client = get_client()
    request = TransactionsSyncRequest(access_token=access_token, cursor=cursor)
    response = client.transactions_sync(request)
    return {
        "added": [_serialize_transaction(t) for t in response['added']],
        "modified": [_serialize_transaction(t) for t in response['modified']],
        "removed": [t['transaction_id'] for t in response['removed']],
        "next_cursor": response['next_cursor'],
        "has_more": response['has_more'],
    }


def _serialize_transaction(txn) -> dict:
    return {
        "plaid_transaction_id": txn['transaction_id'],
        "amount": txn['amount'],
        "category": map_plaid_category(txn['category']),
        "description": txn.get('merchant_name') or txn.get('name'),
        "expense_date": str(txn['date']),
        "source": "plaid",
    }


def map_plaid_category(plaid_categories: list) -> str:
    if not plaid_categories:
        return "Other"
    top_level = plaid_categories[0]
    mapping = {
        "Food and Drink": "Dining",
        "Groceries": "Groceries",
        "Rent": "Rent",
        "Payment": "Rent",
        "Utilities": "Utilities",
        "Travel": "Transportation",
        "Transportation": "Transportation",
        "Recreation": "Entertainment",
        "Entertainment": "Entertainment",
        "Shops": "Shopping",
        "Healthcare": "Health",
        "Service": "Subscriptions",
    }
    return mapping.get(top_level, "Other")