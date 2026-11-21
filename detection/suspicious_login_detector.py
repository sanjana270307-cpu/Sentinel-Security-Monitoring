from database.connection import create_connection
from services.alert_service import create_alert
def detect_suspicious_login():

    db = None
    cursor = None

    try:
        db = create_connection()
        cursor = db.cursor()

        query = """
            SELECT e.user_id, COUNT(f.event_id)
            FROM login_events e
            JOIN login_events f
            ON e.user_id = f.user_id
            AND f.success = 0
            AND f.event_time >= DATE_SUB(e.event_time, INTERVAL 10 MINUTE)
            AND (
                f.event_time < e.event_time
                OR (f.event_time = e.event_time AND f.event_id < e.event_id)
            )
            AND NOT EXISTS (
                SELECT 1
                FROM login_events s
                WHERE s.user_id = e.user_id
                AND s.success = 1
                AND (
                    s.event_time > f.event_time
                    OR (s.event_time = f.event_time AND s.event_id > f.event_id)
                )
                AND (
                    s.event_time < e.event_time
                    OR (s.event_time = e.event_time AND s.event_id < e.event_id)
                )
            )
            WHERE e.success = 1
            AND e.user_id IS NOT NULL
            AND e.event_time >= DATE_SUB(NOW(), INTERVAL 10 MINUTE)
            GROUP BY e.event_id, e.user_id
            HAVING COUNT(f.event_id) >= 5
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
            cursor.execute(check_query,(user_id, "SUSPICIOUS_LOGIN"))
            existing_alert = cursor.fetchone()

            if existing_alert is None:
                result = create_alert(user_id,"high",f"Successful login after {failed_count} failed attempts","SUSPICIOUS_LOGIN")

                if not result:
                    print("Failed to create suspicious login alert")
            else:
                print(f"Active suspicious login alert already exists for user {user_id}")

            if user_id not in detected_users:
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
