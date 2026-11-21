from database.connection import create_connection

def record_audit_log(actor_user_id, action, target_type, target_id, details):

    db = None
    cursor = None

    try:
        db = create_connection()
        cursor = db.cursor()
        query = """
        INSERT INTO audit_logs
        (actor_user_id, action, target_type, target_id, details)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query,(actor_user_id, action, target_type, target_id, details))
        db.commit()

        return True

    except Exception as e:
        print("Audit Log Error:", e)
        return False

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def get_all_audit_logs():
    db = None
    cursor = None

    try:
        db = create_connection()
        cursor = db.cursor()
        query = """SELECT audit_id, actor_user_id, action,
            target_type, target_id, details, created_at
            FROM audit_logs
            ORDER BY created_at DESC
            """
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    except Exception as e:
        print("Audit Log Retrieval Error:", e)
        return []

    finally:
        if cursor:
            cursor.close()

        if db:
            db.close()
