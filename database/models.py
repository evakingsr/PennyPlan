from dataclasses import dataclass
from typing import Optional

@dataclass
class Profile:
    id: str
    name: str
    email: str
    monthly_income: Optional[float] = None

@dataclass
class Expense:
    user_id: str
    category: str
    amount: float
    description: Optional[str] = None
    expense_date: Optional[str] = None

@dataclass
class Budget:
    user_id: str
    category: str
    monthly_limit: float