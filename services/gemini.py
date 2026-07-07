from google import genai
from dotenv import load_dotenv
import os
import re
import json
import time

load_dotenv()

GEMINI_MODELS = ["gemini-2.5-flash", "gemini-3.5-flash"]
MAX_ATTEMPTS = 3
RETRY_SECONDS = 20

_client = None

# Function to get Gemini API Key
def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")
        _client = genai.Client(api_key=api_key)
    return _client

# Helper function to call the Gemini API with retry logic
def _call_gemini_with_retry(prompt: str) -> str:
    client = get_client()
    for model in GEMINI_MODELS:
        for attempt in range(MAX_ATTEMPTS):
            try:
                response = client.models.generate_content(model=model, contents=prompt)
                return response.text.strip()
            except Exception as e:
                print(f"{model} attempt {attempt + 1} failed: {e}. Retrying in ...")
                time.sleep(RETRY_SECONDS)
    raise RuntimeError("All attempts to call Gemini API failed.")

def _build_report_prompt(this_month: dict, last_month: dict) -> str:
    return f"""

    You are a budgeting assistant for a personal finance app called PennyPlan
    Here ihs a user's spending data, already aggreated by category.

    this month by category (USD): {json.dumps(this_month['by_category'])}
    this month total: {this_month['total']}
    last month by category (USD): {json.dumps(last_month['by_category'])}
    last month total: {last_month['total']}

    return ONLY JSON object with exactly these fields, no markdown formatting, no code fences, no extra commentary:
    {{
        "summary": "one paragraph overview of this month's spending"
        "trends": [
            {{"category": "...", "change_percent": ..., "direction": "up" or "down"}}
        ]
        "tips": ["tip 1", "tip 2", "tip 3"]
    }}

    Only include a category in "trends" if it changed by 15% or more versus last month.
    Base "tips" on the categories with the highest spending or the biggest increases.
    """

def _extract_json(raw_text: str) -> dict:
    cleaned = re.sub(r'^```(?:json)?\s*|\s*```$', '', raw_text.strip())
    return json.loads(cleaned)

def _fallback_report(this_month: dict) -> dict:
    top_category = max(this_month['by_category'], key=this_month['by_category'].get, default="spending")
    return {
        "summary": f"You spent ${this_month['total']} this month, mostly on {top_category}.",
        "trends": [],
        "tips": ["Review your largest spending category and look for one recurring cost to cut."],
    }

def generate_report(this_month: dict, last_month: dict) -> dict:
    prompt = _build_report_prompt(this_month, last_month)
    try:
        raw_text = _call_gemini_with_retry(prompt)
        return _extract_json(raw_text)
    except (RuntimeError, json.JSONDecodeError) as e:
        print(f"generate_report falling back: {e}")
        return _fallback_report(this_month)

def categorize_manual_entry(description: str, amount: float) -> str:
    prompt = f"""
    Classify this expense into exactly one category from this list:
    Groceries, Dining, Rent, Utilities, Transportation, Entertainment, Shopping,
    Health, Subscriptions, Other.

    Expense: "{description}", amount: ${amount}

    Return only the category name, nothing else.
    """
    try:
        return _call_gemini_with_retry(prompt)
    except RuntimeError:
        return "Other"
