import bcrypt
from database.connection import create_connection
from services.login_log_service import log_login_event
from services.audit_service import record_audit_log

def hash_password(pwd):

    p = bcrypt.hashpw(pwd.encode("UTF-8"),bcrypt.gensalt())
    return p


def verify_password(password, stored_hash):
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode("UTF-8")
    result = bcrypt.checkpw(password.encode("UTF-8"),stored_hash)
    print(result)
    return result

def register_user(username, password):

    hashed_password = hash_password(password).decode("UTF-8")
    db = None
    cursor = None
    try:
        db = create_connection()
        cursor = db.cursor()
        query = "INSERT into users (username, password_hash, role) values (%s, %s, %s)"
        cursor.execute(query,(username, hashed_password, "Analyst"))
        db.commit()
        print("User registered successfully")
        return True

    except Exception as e:
        print("Registration Error:", e)
        return False

    finally:
        if cursor:
            cursor.close()

        if db:
            db.close()


def login_user(username, password):
    db = None
    cursor = None

    try:
        db = create_connection()
        cursor = db.cursor()
        query = "SELECTuser_id,username,role,password_hash,(locked_until > NOW()),(locked_until IS NOT NULL AND locked_until <= NOW()) FROM users WHERE username = %s "
        cursor.execute(query, (username,))
        row = cursor.fetchone()

        if row is None:
            log_login_event(username,None,False,"Unknown username","Desktop")
            return None

        user_id = row[0]
        stored_username = row[1]
        role = row[2]
        stored_hash = row[3]
        is_locked = row[4]
        lock_expired = row[5]
        if lock_expired:
            reset_failed_attempts(username)

        if is_locked:
            log_login_event(username,user_id,False,"Account locked","Desktop")
            record_audit_log(user_id,"LOGIN_BLOCKED","USER",user_id,"Login attempt blocked because account is locked")

            return None

        if verify_password(password, stored_hash):

            reset_failed_attempts(username)
            record_audit_log(user_id,"LOGIN_SUCCESS","USER",user_id,"User logged in successfully")

            log_login_event(username,user_id,True,None,"Desktop")

            return {"user_id": user_id,"username": stored_username,"role": str(role).strip().lower()}

        else:

            record_failed_attempt(username)
            record_audit_log(user_id,"LOGIN_FAILED","USER",user_id,"Incorrect password entered")
            log_login_event(username,user_id,False,"Incorrect password","Desktop")

            return None

    except Exception as e:

        print("Login Error:", e)
        return None

    finally:

        if cursor:
            cursor.close()
        if db:
            db.close()


def record_failed_attempt(username):

    db = None
    cursor = None

    try:
        db = create_connection()
        cursor = db.cursor()

        query = """
        UPDATE users
        SET failed_attempts = failed_attempts + 1
        WHERE username = %s
        """
        cursor.execute(query, (username,))
        db.commit()
        query = """
        SELECT failed_attempts
        FROM users
        WHERE username = %s
        """
        cursor.execute(query, (username,))
        row = cursor.fetchone()
        if row is None:
            return False

        if row[0] >= 5:
            query = """
            UPDATE users
            SET locked_until = DATE_ADD(NOW(), INTERVAL 5 MINUTE)
            WHERE username = %s
            """
            cursor.execute(query, (username,))
            db.commit()

        return True

    except Exception as e:
        print("Failed Attempt Error:", e)
        return False

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def reset_failed_attempts(username):
    db = None
    cursor = None

    try:
        db = create_connection()
        cursor = db.cursor()
        query = """
        UPDATE users
        SET failed_attempts = 0,
            locked_until = NULL
        WHERE username = %s
        """
        cursor.execute(query, (username,))
        db.commit()
        return True

    except Exception as e:
        print("Reset Failed Attempts Error:", e)
        return False

    finally:
        if cursor:
            cursor.close
        if db:
            db.close()
