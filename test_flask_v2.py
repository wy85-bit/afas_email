import threading
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta

app = Flask(__name__)

# --- CONFIG ---
SECRET_KEY = "5BA4B542D3654105BCDB197D8FE4A23C"
SECURITY_SALT = "copy-hours-v1"
AFAS_TOKEN = "PHRva2VuPjx2ZXJzaW9uPjE8L3ZlcnNpb24+PGRhdGE+NEM1NDMzNDNBRjI0NEE0MjhFMTM3MTIyNzdCREQ1ODQxMUU1MzMyODdGQzI0QUU5QTFBQkQwN0YzNjk1MDM5MzwvZGF0YT48L3Rva2VuPg=="
AFAS_BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"
RENDER_URL = "https://your-app-name.onrender.com"

# Email Server Config (Example using Gmail)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "winnifred.yap@gmail.com"
EMAIL_PASSWORD = 'rhtf ruvr eccw iwok' # Use an 'App Password', not your real password!

serializer = URLSafeTimedSerializer(SECRET_KEY)

# --- 1. THE EMAIL SENDER ---
def send_sync_email(target_email, name, token):
    personal_link = f"{RENDER_URL}/copy-hours?token={token}"
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "🕒 Confirm your hours for last week"
    msg["From"] = f"AFAS Automation <{EMAIL_SENDER}>"
    msg["To"] = target_email

    # Professional HTML Button
    html = f"""
    <html>
      <body style="font-family: sans-serif; line-height: 1.6;">
        <h2>Hi {name},</h2>
        <p>Your hours for last week are ready to be copied to the current week.</p>
        <p>Please click the button below to confirm and sync your time registration.</p>
        <a href="{personal_link}" 
           style="background-color: #007bff; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; display: inline-block;">
           Copy My Hours
        </a>
        <br><br>
        <p>This link will expire in 48 hours.</p>
      </body>
    </html>
    """
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email to {target_email}: {e}")
        return False

# --- 2. THE BACKGROUND WORKER ---
def afas_worker_task(user_id):
    headers = {'Authorization': f'AfasToken {AFAS_TOKEN}', 'Content-Type': 'application/json'}
    try:
        today = datetime.now()
        last_monday = (today - timedelta(days=today.weekday() + 7)).strftime('%Y-%m-%d')
        last_sunday = (today - timedelta(days=today.weekday() + 1)).strftime('%Y-%m-%d')

        get_url = (
            f"{AFAS_BASE_URL}/connectors/Profit_Realization"
            f"?filterfieldids=EmployeeId,DateTime"
            f"&filtervalues={user_id},{last_monday};{last_sunday}"
            f"&operatortypes=1,9"
        )
        source_data = requests.get(get_url, headers=headers).json().get('rows', [])

        for entry in source_data:
            new_date = (datetime.strptime(entry['Da'], '%Y-%m-%d') + timedelta(days=7)).strftime('%Y-%m-%d')
            payload = {
                "PtRealization": {
                    "Element": {
                        "Fields": {
                            "DaTi": new_date,
                            "EmId": user_id,
                            "PrId": entry.get('PrId', '82'),
                            "StTi": entry.get('StTi', '09:00:00'),
                            "EnTi": entry.get('EnTi', '17:00:00'),
                            "Ap": True, "Pr": True
                        }
                    }
                }
            }
            requests.post(f"{AFAS_BASE_URL}/connectors/PtRealization", json=payload, headers=headers)
        print(f"[{user_id}] Sync finished.")
    except Exception as e:
        print(f"[{user_id}] Error: {str(e)}")

# --- 3. THE ROUTES ---

@app.route('/broadcast-org')
def broadcast_org():
    headers = {'Authorization': f'AfasToken {AFAS_TOKEN}'}
    # Ensure your AFAS Connector includes 'Email'
    res = requests.get(f"{AFAS_BASE_URL}/connectors/Employee_List", headers=headers)
    employees = res.json().get('rows', [])

    count = 0
    for emp in employees:
        emp_id = emp['EmployeeId']
        email = emp.get('Email')
        name = emp.get('FirstName', 'Colleague')

        if email:
            token = serializer.dumps(emp_id, salt=SECURITY_SALT)
            if send_sync_email(email, name, token):
                count += 1
        
    return f"Broadcast complete. {count} emails sent."

@app.route('/copy-hours')
def copy_hours():
    token = request.args.get('token')
    try:
        user_id = serializer.loads(token, salt=SECURITY_SALT, max_age=172800)
        thread = threading.Thread(target=afas_worker_task, args=(user_id,), daemon=True)
        thread.start()
        return "✅ Success! Your hours are being synced. You can close this email tab."
    except:
        return "❌ Error: Link expired.", 403

if __name__ == '__main__':
    app.run(port=5000)