from database.connection import create_connection
def get_recent_activity(limit=10):
    db = None
    cursor = None

    try:
        db = create_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                attempted_username,
                event_time,
                success,
                failure_reason,
                source_label
            FROM login_events
            ORDER BY event_time DESC, event_id DESC
            LIMIT %s
        """, (limit,))
        return cursor.fetchall()

    except Exception as e:
        raise RuntimeError("Unable to load recent activity.") from e

    finally:
        if cursor:
            cursor.close()

        if db:
            db.close()