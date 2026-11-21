from services.alert_service import (
    create_alert,
    get_all_alerts,
    update_alert_status,
    delete_alert
)
print("Create:", create_alert(1,"low","Testing alert management","TEST_ALERT"))
alerts = get_all_alerts()
print("Total alerts:", len(alerts))

test_alert_id = None
for alert in alerts:
    if alert[1] == "TEST_ALERT":
        test_alert_id = alert[0]
        break
print("Invalid update:", update_alert_status(9999, "resolved"))
print("Invalid delete:", delete_alert(9999))
print("Delete test alert:", delete_alert(test_alert_id))
