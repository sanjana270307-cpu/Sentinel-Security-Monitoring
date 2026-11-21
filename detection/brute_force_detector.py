from database.connection import create_connection
from services.alert_service import create_alert

def detect_brute_force():

    db = None
    cursor = None

    try:
        db = create_connection()
        cursor = db.cursor()
        query = """
        SELECT user_id, COUNT(*)
        FROM login_events
        WHERE success = 0
        AND user_id IS NOT NULL
        AND event_time >= DATE_SUB(NOW(), INTERVAL 5 MINUTE)
        GROUP BY user_id
        HAVING COUNT(*) >= 5
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        detected_users = []

        for row in rows:
            user_id = row[0]
            failed_count = row[1]
            check_query = """
            SELECT alert_id
            FROM security_alerts
            WHERE related_user_id = %s
            AND rule_code = %s
            AND status IN ('new', 'investigating')
            LIMIT 1
            """
            cursor.execute(check_query, (user_id, "BRUTE_FORCE"))
            existing_alert = cursor.fetchone()

            if existing_alert is None:
                result = create_alert(
                    user_id,
                    "high",
                    f"Brute-force attack detected: {failed_count} failed login attempts in 5 minutes",
                    "BRUTE_FORCE")

                if not result:
                    print("Failed to create security alert")
            else:
                print(f"Active brute-force alert already exists for user {user_id}")

            detected_users.append(user_id)
        return detected_users

    except Exception as e:
        print("Detection Error:", e)
        return []

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

