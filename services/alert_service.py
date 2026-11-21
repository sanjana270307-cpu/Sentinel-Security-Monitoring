from database.connection import create_connection

def create_alert(user_id,severity,description,rule_code):
    db = None
    cursor = None

    try:
        db=create_connection()
        cursor = db.cursor()
        query="INSERT into security_alerts (related_user_id,severity,description,status,rule_code) Values (%s,%s,%s,%s,%s)"
        cursor.execute(query,(user_id,severity,description,"new",rule_code))
        db.commit()
        return True
    except Exception as e:
        print("Alert Creation Error:", e)
        return False
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def get_all_alerts():

    db = None
    cursor = None
    try:
        db=create_connection()
        cursor=db.cursor()
        query = "SELECT * FROM security_alerts ORDER BY created_at DESC"
        cursor.execute(query)
        row = cursor.fetchall()
        return row
    
    except Exception as e:
        print("Alert Creation Error:", e)
        return False
    
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def update_alert_status(alert_id, new_status):
    db=None
    cursor=None
    valid_statuses = ["new", "investigating", "resolved", "dismissed"]

    if new_status not in valid_statuses:
        return False

    try:
        db=create_connection()
        cursor=db.cursor()
        query="UPDATE security_alerts SET status = %s WHERE alert_id = %s"
        cursor.execute(query,(new_status,alert_id))
        db.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False
    
    except Exception as e:
        print("Alert Creation Error:", e)
        return False
    
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def delete_alert(alert_id):

    db = None
    cursor=None

    try:
        db=create_connection()
        cursor=db.cursor()
        query="DELETE FROM security_alerts WHERE alert_id = %s "
        cursor.execute(query,(alert_id,))
        db.commit()
        count=cursor.rowcount
        if count > 0:
            return True
        else:
            return False
    
    except Exception as e:
        print("Alert Creation Error:", e)
        return False
    
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
