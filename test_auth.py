from database.database import sign_up_user, login_user

email = "evaTest@gmail.com"
password = "Password123!"
name = "Eva"

signup = sign_up_user(email, password, name)
print(signup)

login = login_user(email, password)
print(login)

print(login.user.id)