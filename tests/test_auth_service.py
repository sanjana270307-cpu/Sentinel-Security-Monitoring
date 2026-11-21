from services.auth_service import login_user

for i in range(5):
    result = login_user("test_user", "wrongpassword")
    print("Attempt", i + 1, ":", result)