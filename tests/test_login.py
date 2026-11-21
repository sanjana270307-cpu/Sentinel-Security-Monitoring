from services.auth_service import login_user

# First: 3 failed attempts
for i in range(3):
    login_user("test_user", "wrong_password")

# Then: successful login
print("First success:", login_user("test_user", "Test@123"))

# Next: 2 failed attempts
for i in range(2):
    login_user("test_user", "wrong_password")

# Finally: another successful login
print("Second success:", login_user("test_user", "Test@123"))