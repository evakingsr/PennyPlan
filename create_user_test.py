# create_user_test.py
from database import sign_up_user

EMAIL = "pennyplan.test.user@gmail.com"
PASSWORD = "TestPassword123!"
NAME = "Test User"

print("Signing up test user...")
response = sign_up_user(EMAIL, PASSWORD, NAME)
print(response)

user_id = response.user.id
print(f"\nuser_id: {user_id}")

print("\nAttempting login...")
