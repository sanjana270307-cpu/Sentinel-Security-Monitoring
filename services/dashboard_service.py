from database.connection import create_connection

def get_dashboard_stats():
    db = None
    cursor = None

    try:
        db = create_connection()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM login_events")
        login_events = cursor.fetchone()[0]
        cursor.execute("""
            SELECT COUNT(*)
            FROM security_alerts
            WHERE status IN ('new', 'investigating')
        """)
        active_alerts = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM security_alerts")
        threats_detected = cursor.fetchone()[0]

        return {
            "total_users": total_users,
            "login_events": login_events,
            "active_alerts": active_alerts,
            "threats_detected": threats_detected
        }

    except Exception as e:
        raise RuntimeError("Unable to load dashboard statistics.") from e

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
