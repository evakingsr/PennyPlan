from collections import defaultdict
from datetime import date, datetime, timedelta

def aggregate_spending(expenses:list, period: str = 'this_month') -> dict:
    start, end = _period_bounds(period)
    filtered = [e for e in expenses if start <= _parse_date(e['expense_date']) < end]

    by_category = defaultdict(float)
    for e in filtered:
        by_category[e['category']] += e['amount']
    
    return{
        "total": round(sum(by_category.values()), 2),
        "by_category": {k: round(v, 2) for k, v in by_category.items()}
    }

def _parse_date(value) -> date:
    if isinstance(value, date):
        return value
    return datetime.fromisoformat(value).date()

def _period_bounds(period: str) -> tuple:
    today = date.today()
    first_of_this_month = today.replace(day=1)
    if period == 'this_month':
        return first_of_this_month, today + timedelta(days=1)
    elif period == 'last_month':
        last_month_end = first_of_this_month
        last_month_start = (first_of_this_month - timedelta(days=1)).replace(day=1)
        return last_month_start, last_month_end
    else:
        raise ValueError(f"Unknown period: {period}")
