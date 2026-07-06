import os
from detenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("https://mxozyqicudixrkfqlxgt.supabase.co")
SUPABASE_KEY = os.getenv("sb_publishable_LM4Zh7XmF8y6hdmsVBRpag_FQCvR8D0")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def add_user(name, email):
    response = supabase.table("users").insert({
        "name" : name,
        "email" : email
    }).execute()
    return response.data

def add_budget(user_id, category, monthly_limit):
    reponse = supabase.table("budgets").insert({
        "user_id" : user_id,
        "category" : cvategory,
        "monthly_limit" : monthly_limit
    }).execute()
    return response.data

def add_expense(user_id, category, description, amount, expense_data):
    response = supabase.table("expenses").insert({
        "user_id" : user_id,
        "category" : category,
        "description" : description,
        "amount" : amount,
        "expense_date" : expense_data
    }).execute()
    return response.data
def get_expenses(user_id):
    response = supabse.table("expenses").select("*").eq("user_id", user_id).execute()
    return response.data

def get_budgets(user_id):
    response = supabase.table("budgets").select("*").eq("user_id", user_id).execute()
    return response.data