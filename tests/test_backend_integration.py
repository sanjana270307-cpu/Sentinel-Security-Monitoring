'''from datetime import datetime
from services.auth_service import register_user, login_user

username = "sentinel_test_" + datetime.now().strftime("%H%M%S")
password = "SentinelTest@123"
print("Starting Backend Integration Test")
registered = register_user(username, password)
print("User Registration:", registered)
if registered:
    login_result = login_user(username, password)
    print("User Login:", login_result)'''

from services.auth_service import login_user

print("\nTesting suspicious activity...")

result = login_user("test_user", "Test@123")
print(f"Correcy attempt 1:", result)