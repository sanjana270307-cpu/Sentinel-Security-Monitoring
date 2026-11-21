from services.audit_service import (record_audit_log,get_all_audit_logs)
print("Record:", record_audit_log(1,"TEST_ACTION","USER",1,"Testing audit service"))
logs = get_all_audit_logs()
print("Total logs:", len(logs))
if logs:
    print("Latest log:", logs[0])

