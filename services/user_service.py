from database.connection import create_connection

def get_all_users():
    db = None
    cursor = None

    try:
        db = create_connection()
        cursor = db.cursor(dictionary=True)
        query = """
            SELECT user_id, username, role,
                failed_attempts, locked_until
            FROM users
            ORDER BY user_id DESC
            """
        cursor.execute(query)
        return cursor.fetchall()

    except Exception as e:
        print("User Retrieval Error:", e)
        return []

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def unlock_user(user_id):
    db = None
    cursor = None

    try:
        db = create_connection()
        cursor = db.cursor()
        query = """
        UPDATE users
        SET failed_attempts = 0,
            locked_until = NULL
        WHERE user_id = %s
        """
        cursor.execute(query, (user_id,))
        db.commit()

        return cursor.rowcount > 0

    except Exception as e:
        print("User Unlock Error:", e)
        return False

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def update_user_role(user_id, new_role):
    db = None
    cursor = None

    if new_role not in ["Analyst", "Admin"]:
        return False

    try:
        db = create_connection()
        cursor = db.cursor()
        query = """
        UPDATE users
        SET role = %s
        WHERE user_id = %s
        """
        cursor.execute(query, (new_role, user_id))
        db.commit()

        return cursor.rowcount > 0

    except Exception as e:
        print("Role Update Error:", e)
        return False

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
