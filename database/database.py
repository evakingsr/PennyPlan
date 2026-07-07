import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def sign_up_user(email, password, name):
    response = supabase.auth.sign_up({
        "email" : email,
        "password" : password,
        "options" : {
            "data" : {
                "name" : name
            }
        }
    })
    return response.data

def login_user(email, password):
    response = supabase.auth.sign_in_with_password({
        "email" : email,
        "password" : password
    })
    return response

def get_user_id(login_response):
    return login_response.user.id

def get_profile(user_id):
    response = (
        supabase.table("profiles")
        .select("*")
        .eq("id", user_id)
        .execute()
    )
    return response.data

def update_monthly_income(user_id, monthly_income):
    response = (
        supabase.table("profiles")
        .update({"monthly_income": monthly_income})
        .eq("id", user_id)
        .execute()
    )
    return response.data

def add_budget(user_id, category, monthly_limit):
    response = supabase.table("budgets").insert({
        "user_id" : user_id,
        "category" : category,
        "monthly_limit" : monthly_limit
    }).execute()
    return response

def get_budgets(user_id):
    response = (
        supabase.table("budgets")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
    return response.data

def add_expense(user_id, category, description, amount, expense_date):
    response = supabase.table("expenses").insert({
        "user_id" : user_id,
        "category" : category,
        "description" : description,
        "amount" : amount,
        "expense_date" : expense_date
    }).execute()
    return response.data

def get_expenses(user_id):
    response = (
        supabase.table("expenses")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
    return response.data

def delete_expense(expense_id):
    response = (
        supabase.table("expenses")
        .delete()
        .eq("id", expense_id)
        .execute()
    )
    return response.data

def update_expense(expense_id, category, description, amount, expense_date):
    response = (
        supabase.table("expenses")
        .update({
            "category" : category,
            "description" : description,
            "amount" : amount,
            "expense_date" : expense_date
        })
        .eq("id", expense_id)
        .execute()
    )
    return response.data