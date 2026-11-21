from database.connection import create_connection
from detection.run_detection import run_all_detections

def main():
    print("================================")
    print("       SENTINEL SECURITY")
    print("================================")
    db = None
    try:
        db = create_connection()
        print("Database connection successful!")

    except Exception as e:
        print("Database connection failed:", e)
        return

    finally:
        if db:
            db.close()

    print("\nStarting security monitoring...\n")
    run_all_detections()
    print("\nSentinel execution completed!")

if __name__ == "__main__":
    main()
