from database.connection import create_connection

def log_login_event(username, user_id, success, failure_reason, source_label):
    db = None
    cursor = None

    try :
        db = create_connection()
        cursor = db.cursor()
        query = "INSERT INTO login_events(user_id, attempted_username, failure_reason, success, source_label) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query,(user_id,username,failure_reason,success,source_label))
        db.commit()
        return True
    
    except Exception as e:
        print("Login Event Logging Error:", e)
        return False
    
    finally :
        if cursor:
            cursor.close()
        if db:
            db.close()
