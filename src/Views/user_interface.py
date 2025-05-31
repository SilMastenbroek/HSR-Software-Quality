from src.Controllers.logger import get_unread_suspicious_logs

def post_login_notice(user_role):
    if user_role in ["super_admin", "system_admin"]:
        alerts = get_unread_suspicious_logs()
        if alerts:
            print("Let op: login activiteit gefaald:")
            for log in alerts:
                print(" -", " | ".join(log))
