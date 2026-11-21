from services.login_log_service import log_login_event
result=log_login_event("test_user",1,True,None,"Desktop")
print(result)