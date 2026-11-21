from detection.brute_force_detector import detect_brute_force
from detection.suspicious_login_detector import detect_suspicious_login
def run_all_detections():

    print("Starting Sentinel Detection Engine...")
    brute_force_users = detect_brute_force()
    suspicious_users = detect_suspicious_login()
    results = {"brute_force": brute_force_users or [],"suspicious_login": suspicious_users or []}

    print("\nDetection Results")
    print("-------------------------")
    print("Brute-force detected users:", results["brute_force"])
    print("Suspicious login detected users:", results["suspicious_login"])
    print("\nDetection Engine Completed!")

    return results

if __name__ == "__main__":
    run_all_detections()
