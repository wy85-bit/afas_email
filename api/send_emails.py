from http.server import BaseHTTPRequestHandler
import base64
import requests
import json
import smtplib
from email.message import EmailMessage

# --- CONFIGURATION ---
# Use the exact XML token you provided earlier
AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
AFAS_URL = "https://90114.resttest.afas.online/ProfitRestServices/connectors/Profit_Realization"

# --- GMAIL SETTINGS ---
GMAIL_USER = "your-email@gmail.com"  # <--- Change to your Gmail address
GMAIL_APP_PASS = "your-16-char-code" # <--- Change to your App Password

def get_afas_headers():
    """Encodes the token for AFAS authorization."""
    encoded_token = base64.b64encode(AFAS_TOKEN_XML.encode('utf-8')).decode('utf-8')
    return {
        'Authorization': f'AfasToken {encoded_token}',
        'Content-Type': 'application/json'
    }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # 1. Fetch data from AFAS to ensure we have something to "send"
            headers = get_afas_headers()
            afas_resp = requests.get(AFAS_URL, headers=headers)
            
            if afas_resp.status_code != 200:
                raise Exception(f"AFAS Error: {afas_resp.status_code}")

            data = afas_resp.json()
            rows = data.get('rows', [])
            sample_count = len(rows) #

            # 2. Construct the email for YOU
            msg = EmailMessage()
            msg.set_content(f"""
            Hi Winnie! 
            
            This is a successful test from Vercel. 
            The system currently sees {sample_count} hour records in AFAS environment 90114.
            
            When you are ready, we will loop this to send to your 50 colleagues!
            """)
            
            msg['Subject'] = "🚀 AFAS-Vercel Connection Success!"
            msg['From'] = GMAIL_USER
            msg['To'] = GMAIL_USER # Always sending to yourself for now!

            # 3. Connect to Gmail and SEND
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(GMAIL_USER, GMAIL_APP_PASS)
                smtp.send_message(msg)

            # 4. Success Response to Browser
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            success_json = {
                "status": "Success",
                "message": f"Email sent to {GMAIL_USER}",
                "records_found": sample_count
            }
            self.wfile.write(json.dumps(success_json).encode())

        except Exception as e:
            # Error Response
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "Failed", "error": str(e)}).encode())


# from http.server import BaseHTTPRequestHandler
# import json
# import requests

# class handler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         # --- SAFETY SETTINGS ---
#         MY_PRIVATE_EMAIL = "winnie.yap@veneficus.nl" # <--- PUT YOUR EMAIL HERE!
        
#         # In a real run, we'd loop through all 50 people.
#         # For this test, we are only sending ONE email to YOU.
        
#         try:
#             # This simulates the email logic
#             subject = "Vercel Test: AFAS Hour Update"
#             body = "Hi Winnie, the connection to environment 90114 is working!"
            
#             # Here you would plug in your Email Service (like SendGrid or Mailgun)
#             # For now, we'll just return a success message to the browser.
            
#             response_message = {
#                 "status": "Safety Mode Active",
#                 "recipient": MY_PRIVATE_EMAIL,
#                 "message": "If an email service was connected, it would have sent now!",
#                 "test_data_sample": "Employee 1000077 has entries." #
#             }

#             self.send_response(200)
#             self.send_header('Content-type', 'application/json')
#             self.end_headers()
#             self.wfile.write(json.dumps(response_message).encode())

#         except Exception as e:
#             self.send_response(500)
#             self.end_headers()
#             self.wfile.write(str(e).encode())


# # import requests
# # import json

# # # Your Vercel App URL
# # # VERCEL_APP_URL = "https://your-project-name.vercel.app"
# # VERCEL_APP_URL = 'https://afas-email.vercel.app/''

# # def generate_approval_email(employee_id, employee_name, hours_count):
# #     """Creates the content for the email with the unique approval link."""
# #     # This link points to your Vercel app, which then calls post_hours_for_employee.py
# #     approval_link = f"{VERCEL_APP_URL}/api/approve?user_id={employee_id}"
    
# #     subject = f"Action Required: Copy your hours for this week, {employee_name}?"
# #     body = f"""
# #     Hi {employee_name},
    
# #     We found {hours_count} hour entries from your previous week. 
# #     Would you like to copy these to the current week?
    
# #     Click the link below to authorize the copy:
# #     {approval_link}
    
# #     If you do nothing, no hours will be copied.
# #     """
# #     return subject, body

# # def process_and_notify_all():
# #     # 1. Use your bulk downloader logic
# #     # (Assuming download_all_hours() is imported from your other file)
# #     all_employee_data = download_all_hours() 
    
# #     for emp_id, hours in all_employee_data.items():
# #         # Get the name from the first record if available
# #         emp_name = hours[0].get('Naam', 'Colleague')
# #         count = len(hours)
        
# #         subject, content = generate_approval_email(emp_id, emp_name, count)
        
# #         # 2. Integration with your Email Provider (Example using a generic sender)
# #         print(f"📧 Sending email to {emp_name} ({emp_id}) for {count} hours...")
# #         # send_email(to=emp_email, subject=subject, body=content) 

# # if __name__ == "__main__":
# #     process_and_notify_all()
