from google import genai
from dotenv import load_dotenv
import os
import re
import json
import time


load_dotenv()


GEMINI_MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash",
]

MAX_ATTEMPTS = 3
RETRY_SECONDS = 20

_client = None


# Function to get Gemini API Key
def get_client():
    global _client

    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY environment variable is not set."
            )

        _client = genai.Client(api_key=api_key)

    return _client


# Helper function to call the Gemini API with retry logic
def _call_gemini_with_retry(prompt: str) -> str:
    client = get_client()
    last_error = None

    for model in GEMINI_MODELS:
        for attempt in range(MAX_ATTEMPTS):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )

                if not response.text:
                    raise RuntimeError(
                        f"{model} returned an empty response."
                    )

                return response.text.strip()

            except Exception as error:
                last_error = error

                print(
                    f"{model} attempt {attempt + 1} failed: {error}"
                )

                if attempt < MAX_ATTEMPTS - 1:
                    time.sleep(RETRY_SECONDS)

    raise RuntimeError(
        f"All attempts to call Gemini API failed. Last error: {last_error}"
    )


def _build_report_prompt(
    this_month: dict,
    last_month: dict,
) -> str:
    return f"""
You are a budgeting assistant for a personal finance app called PennyPlan.

Here is a user's spending data, already aggregated by category.

This month by category (USD):
{json.dumps(this_month['by_category'])}

This month total:
{this_month['total']}

Last month by category (USD):
{json.dumps(last_month['by_category'])}

Last month total:
{last_month['total']}

Return ONLY a valid JSON object with exactly these fields.
Do not use Markdown, code fences, or extra commentary.

{{
    "summary": "one paragraph overview of this month's spending",
    "trends": [
        {{
            "category": "...",
            "change_percent": 0,
            "direction": "up"
        }}
    ],
    "tips": [
        "tip 1",
        "tip 2",
        "tip 3"
    ]
}}

The direction value must be either "up" or "down".

Only include a category in "trends" if it changed by 15 percent or more
versus last month.

Base the tips on the categories with the highest spending or the biggest
increases.
"""


def _extract_json(raw_text: str) -> dict:
    cleaned = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        raw_text.strip(),
    )

    return json.loads(cleaned)


def _fallback_report(this_month: dict) -> dict:
    top_category = max(
        this_month["by_category"],
        key=this_month["by_category"].get,
        default="spending",
    )

    return {
        "summary": (
            f"You spent ${this_month['total']} this month, "
            f"mostly on {top_category}."
        ),
        "trends": [],
        "tips": [
            (
                "Review your largest spending category and look "
                "for one recurring cost to cut."
            )
        ],
    }


def generate_report(
    this_month: dict,
    last_month: dict,
) -> dict:
    prompt = _build_report_prompt(
        this_month,
        last_month,
    )

    try:
        raw_text = _call_gemini_with_retry(prompt)
        return _extract_json(raw_text)

    except Exception as error:
        print(f"generate_report falling back: {error}")
        return _fallback_report(this_month)


def categorize_manual_entry(
    description: str,
    amount: float,
) -> str:
    prompt = f"""
Classify this expense into exactly one category from this list:

Groceries, Dining, Rent, Utilities, Transportation, Entertainment,
Shopping, Health, Subscriptions, Other.

Expense: "{description}"
Amount: ${amount}

Return only the category name, nothing else.
"""

    try:
        return _call_gemini_with_retry(prompt)

    except Exception as error:
        print(f"categorize_manual_entry falling back: {error}")
        return "Other"