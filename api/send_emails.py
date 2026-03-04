from http.server import BaseHTTPRequestHandler
import base64, requests, json
from urllib.parse import urlparse, parse_qs

# --- CONFIGURATION ---
AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices/connectors"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Capture the ID from the email button
        query = parse_qs(urlparse(self.path).query)
        user_id = query.get('user_id', [None])[0]
        
        token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
        headers = {'Authorization': f'AfasToken {token}', 'Content-Type': 'application/json'}

        try:
            # 2. Get the source data
            afas_resp = requests.get(f"{BASE_URL}/Profit_Realization", headers=headers)
            all_rows = afas_resp.json().get('rows', [])
            
            # Filter for our specific employee
            my_rows = [r for r in all_rows if str(r.get('EmployeeId')) == str(user_id)]
            
            # 3. Use a date we KNOW is open in 90114
            safe_date = "2021-01-01" 
            
            success_count = 0
            error_msg = ""

            # 4. Push to AFAS UpdateConnector
            for row in my_rows:
                payload = {
                    "PtRealization": {
                        "Element": {
                            "Fields": {
                                "EmId": row.get('EmployeeId'),
                                "PrId": row.get('ProjectID'),
                                "ItId": row.get('ItemCodeId'),
                                "UnId": row.get('UnitId'),
                                "Qu": row.get('QuantityUnit'),
                                "Da": safe_date  # Overriding to use the open period
                            }
                        }
                    }
                }
                
                post_resp = requests.post(f"{BASE_URL}/PtRealization", headers=headers, json=payload)
                
                if post_resp.status_code in [200, 201]:
                    success_count += 1
                else:
                    # Capture specific AFAS rejection reasons
                    error_msg = post_resp.json().get('externalMessage', 'Validation Error')

            # 5. Success Page with clear feedback
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            status_icon = "✅" if success_count > 0 else "❌"
            title = "Success!" if success_count > 0 else "Action Needed"
            
            html = f"""
            <html>
                <head><meta charset="UTF-8"></head>
                <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                    <h1 style="color: #0070f3;">{status_icon} {title}</h1>
                    <p style="font-size: 1.2em;">Processed <b>{success_count}</b> entries for Employee <b>{user_id}</b>.</p>
                    {f'<p style="color:red"><b>AFAS Error:</b> {error_msg}</p>' if error_msg and success_count == 0 else ''}
                    <p style="color: #666;">Target Date: {safe_date} | Source Records: {len(my_rows)}</p>
                </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"System Error: {str(e)}".encode())


# from http.server import BaseHTTPRequestHandler
# import base64, requests, json
# from urllib.parse import urlparse, parse_qs

# # --- CONFIGURATION ---
# AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
# BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices/connectors"

# class handler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         # 1. Get the Employee ID from the button click
#         query = parse_qs(urlparse(self.path).query)
#         user_id = query.get('user_id', [None])[0]
        
#         # 2. Prepare Headers
#         token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
#         headers = {'Authorization': f'AfasToken {token}', 'Content-Type': 'application/json'}

#         try:
#             # 3. Fetch all rows to find our specific employee
#             afas_resp = requests.get(f"{BASE_URL}/Profit_Realization", headers=headers)
#             all_rows = afas_resp.json().get('rows', [])
#             my_rows = [r for r in all_rows if str(r.get('EmployeeId')) == str(user_id)]
            
#             # 4. Use a known "Open" date to avoid the Period Error
#             safe_date = "2021-01-01" 
            
#             success_count = 0
#             error_message = ""

#             # 5. Push to AFAS UpdateConnector
#             for row in my_rows:
#                 payload = {
#                     "PtRealization": {
#                         "Element": {
#                             "Fields": {
#                                 "EmId": row.get('EmployeeId'),   #
#                                 "PrId": row.get('ProjectID'),    #
#                                 "ItId": row.get('ItemCodeId'),   #
#                                 "UnId": row.get('UnitId'),       #
#                                 "Qu": row.get('QuantityUnit'),   #
#                                 "Da": safe_date                  # Fixed Date
#                             }
#                         }
#                     }
#                 }
                
#                 post_resp = requests.post(f"{BASE_URL}/PtRealization", headers=headers, json=payload)
                
#                 if post_resp.status_code in [200, 201]:
#                     success_count += 1
#                 else:
#                     # Capture the AFAS error message if it fails
#                     error_data = post_resp.json()
#                     error_message = error_data.get('externalMessage', 'Validation Error')

#             # 6. Build the Response Page
#             self.send_response(200)
#             self.send_header('Content-type', 'text/html; charset=utf-8')
#             self.end_headers()
            
#             status_icon = "✅" if success_count > 0 else "❌"
#             title = "Success!" if success_count > 0 else "Action Needed"
            
#             html = f"""
#             <html>
#                 <head><meta charset="UTF-8"></head>
#                 <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
#                     <h1 style="color: #0070f3;">{status_icon} {title}</h1>
#                     <p style="font-size: 1.2em;">Processed <b>{success_count}</b> entries for Employee <b>{user_id}</b>.</p>
#                     {f'<p style="color:red"><b>AFAS says:</b> {error_message}</p>' if error_message and success_count == 0 else ''}
#                     <p style="color: #666;">Date used for entry: {safe_date}</p>
#                     <p>Found {len(my_rows)} source records in AFAS.</p>
#                 </body>
#             </html>
#             """
#             self.wfile.write(html.encode('utf-8'))

#         except Exception as e:
#             self.send_response(500)
#             self.end_headers()
#             self.wfile.write(f"System Error: {str(e)}".encode())


# # from http.server import BaseHTTPRequestHandler
# # import base64, requests, json, smtplib
# # from email.message import EmailMessage

# # # --- CONFIG ---
# # AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
# # AFAS_URL = "https://90114.resttest.afas.online/ProfitRestServices/connectors/Profit_Realization"
# # GMAIL_USER = "winnifred.yap@gmail.com" 
# # GMAIL_APP_PASS = "rhtf ruvr eccw iwok" 

# # class handler(BaseHTTPRequestHandler):
# #     def do_GET(self):
# #         try:
# #             # 1. Get AFAS data
# #             token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
# #             resp = requests.get(AFAS_URL, headers={'Authorization': f'AfasToken {token}'})
# #             rows = resp.json().get('rows', [])
            
# #             # 2. Fix the Key: It's 'EmployeeId' in your data!
# #             emp_id = rows[0].get('EmployeeId', '90114') if rows else '90114'

# #             # 3. HTML Content
# #             html = f"""
# #             <html><body style="font-family: sans-serif;">
# #                 <h2>Hi Winnie! 🕒</h2>
# #                 <p>Ready to copy hours for <b>{emp_id}</b>?</p>
# #                 <a href="https://afas-email.vercel.app/api/approve?user_id={emp_id}" 
# #                    style="background: #0070f3; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px;">
# #                    🚀 Copy my hours
# #                 </a>
# #             </body></html>
# #             """
# #             msg = EmailMessage()
# #             msg['Subject'], msg['From'], msg['To'] = "AFAS Test", GMAIL_USER, GMAIL_USER
# #             msg.set_content("Use an HTML client."); msg.add_alternative(html, subtype='html')

# #             with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
# #                 smtp.login(GMAIL_USER, GMAIL_APP_PASS)
# #                 smtp.send_message(msg)

# #             self.send_response(200)
# #             self.end_headers()
# #             self.wfile.write(b"Email sent! Check your inbox.")
# #         except Exception as e:
# #             self.send_response(500)
# #             self.end_headers()
# #             self.wfile.write(str(e).encode())



# # # from http.server import BaseHTTPRequestHandler
# # # import base64
# # # import requests
# # # import json
# # # import smtplib
# # # from email.message import EmailMessage

# # # # --- YOUR SAVED CONFIG ---
# # # AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
# # # AFAS_URL = "https://90114.resttest.afas.online/ProfitRestServices/connectors/Profit_Realization"

# # # # --- CREDENTIALS (Double check these!) ---
# # # GMAIL_USER = "winnifred.yap@gmail.com"
# # # GMAIL_APP_PASS = "rhtf ruvr eccw iwok" # Your 16-character Gmail App Password

# # # class handler(BaseHTTPRequestHandler):
# # #     def do_GET(self):
# # #         try:
# # #             # 1. Fetch data from AFAS
# # #             encoded_token = base64.b64encode(AFAS_TOKEN_XML.encode('utf-8')).decode('utf-8')
# # #             afas_resp = requests.get(AFAS_URL, headers={'Authorization': f'AfasToken {encoded_token}'})
# # #             data = afas_resp.json()
# # #             rows = data.get('rows', [])
            
# # #             # Let's use the first employee ID we find in your data
# # #             sample_id = rows[0].get('Medewerker', 'Unknown') if rows else '90114'

# # #             # 2. Build the HTML Email with a styled button
# # #             html_content = f"""
# # #             <html>
# # #                 <body style="font-family: sans-serif; padding: 20px;">
# # #                     <h2 style="color: #333;">Action Required: AFAS Hour Update</h2>
# # #                     <p>Hi Winnie! We found your hours in environment 90114.</p>
# # #                     <p>Click the button below to copy them automatically:</p>
# # #                     <div style="margin-top: 25px;">
# # #                         <a href="https://afas-email.vercel.app/api/approve?user_id={sample_id}" 
# # #                            style="background: #0070f3; color: white; padding: 14px 25px; text-decoration: none; border-radius: 6px; font-weight: bold;">
# # #                            🚀 Copy Hours for {sample_id}
# # #                         </a>
# # #                     </div>
# # #                 </body>
# # #             </html>
# # #             """

# # #             # 3. Setup the Email message
# # #             msg = EmailMessage()
# # #             msg['Subject'] = "🚀 Test: Copy your AFAS Hours"
# # #             msg['From'] = GMAIL_USER
# # #             msg['To'] = GMAIL_USER # Keeping it safe—sending to YOU!
# # #             msg.set_content("Please view this in an HTML-compatible email client.")
# # #             msg.add_alternative(html_content, subtype='html')

# # #             # 4. Send it!
# # #             with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
# # #                 smtp.login(GMAIL_USER, GMAIL_APP_PASS)
# # #                 smtp.send_message(msg)

# # #             self.send_response(200)
# # #             self.send_header('Content-type', 'application/json')
# # #             self.end_headers()
# # #             self.wfile.write(json.dumps({{"status": "Success", "sent_to": GMAIL_USER}}).encode())

# # #         except Exception as e:
# # #             self.send_response(500)
# # #             self.send_header('Content-type', 'application/json')
# # #             self.end_headers()
# # #             self.wfile.write(json.dumps({{"error": str(e)}}).encode())



# # # # from http.server import BaseHTTPRequestHandler
# # # # import base64
# # # # import requests
# # # # import json
# # # # import smtplib
# # # # from email.message import EmailMessage

# # # # # --- CONFIGURATION ---
# # # # # Use the exact XML token you provided earlier
# # # # AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
# # # # AFAS_URL = "https://90114.resttest.afas.online/ProfitRestServices/connectors/Profit_Realization"

# # # # # --- GMAIL SETTINGS ---
# # # # GMAIL_USER = "winnifred.yap@gmail.com"  # <--- Change to your Gmail address
# # # # GMAIL_APP_PASS = "rhtf ruvr eccw iwok"
# # # # # <--- Change to your App Password

# # # # def get_afas_headers():
# # # #     """Encodes the token for AFAS authorization."""
# # # #     encoded_token = base64.b64encode(AFAS_TOKEN_XML.encode('utf-8')).decode('utf-8')
# # # #     return {
# # # #         'Authorization': f'AfasToken {encoded_token}',
# # # #         'Content-Type': 'application/json'
# # # #     }

# # # # class handler(BaseHTTPRequestHandler):
# # # #     def do_GET(self):
# # # #         try:
# # # #             # 1. Fetch data from AFAS to ensure we have something to "send"
# # # #             headers = get_afas_headers()
# # # #             afas_resp = requests.get(AFAS_URL, headers=headers)
            
# # # #             if afas_resp.status_code != 200:
# # # #                 raise Exception(f"AFAS Error: {afas_resp.status_code}")

# # # #             data = afas_resp.json()
# # # #             rows = data.get('rows', [])
# # # #             sample_count = len(rows) #

# # # #             # 2. Construct the email for YOU
# # # #             msg = EmailMessage()
# # # #             msg.set_content(f"""
# # # #             Hi Winnie! 
            
# # # #             This is a successful test from Vercel. 
# # # #             The system currently sees {sample_count} hour records in AFAS environment 90114.
            
# # # #             When you are ready, we will loop this to send to your 50 colleagues!
# # # #             """)
            
# # # #             msg['Subject'] = "🚀 AFAS-Vercel Connection Success!"
# # # #             msg['From'] = GMAIL_USER
# # # #             msg['To'] = GMAIL_USER # Always sending to yourself for now!

# # # #             # 3. Connect to Gmail and SEND
# # # #             with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
# # # #                 smtp.login(GMAIL_USER, GMAIL_APP_PASS)
# # # #                 smtp.send_message(msg)

# # # #             # 4. Success Response to Browser
# # # #             self.send_response(200)
# # # #             self.send_header('Content-type', 'application/json')
# # # #             self.end_headers()
# # # #             success_json = {
# # # #                 "status": "Success",
# # # #                 "message": f"Email sent to {GMAIL_USER}",
# # # #                 "records_found": sample_count
# # # #             }
# # # #             self.wfile.write(json.dumps(success_json).encode())

# # # #         except Exception as e:
# # # #             # Error Response
# # # #             self.send_response(500)
# # # #             self.send_header('Content-type', 'application/json')
# # # #             self.end_headers()
# # # #             self.wfile.write(json.dumps({"status": "Failed", "error": str(e)}).encode())


# # # # # from http.server import BaseHTTPRequestHandler
# # # # # import json
# # # # # import requests

# # # # # class handler(BaseHTTPRequestHandler):
# # # # #     def do_GET(self):
# # # # #         # --- SAFETY SETTINGS ---
# # # # #         MY_PRIVATE_EMAIL = "winnie.yap@veneficus.nl" # <--- PUT YOUR EMAIL HERE!
        
# # # # #         # In a real run, we'd loop through all 50 people.
# # # # #         # For this test, we are only sending ONE email to YOU.
        
# # # # #         try:
# # # # #             # This simulates the email logic
# # # # #             subject = "Vercel Test: AFAS Hour Update"
# # # # #             body = "Hi Winnie, the connection to environment 90114 is working!"
            
# # # # #             # Here you would plug in your Email Service (like SendGrid or Mailgun)
# # # # #             # For now, we'll just return a success message to the browser.
            
# # # # #             response_message = {
# # # # #                 "status": "Safety Mode Active",
# # # # #                 "recipient": MY_PRIVATE_EMAIL,
# # # # #                 "message": "If an email service was connected, it would have sent now!",
# # # # #                 "test_data_sample": "Employee 1000077 has entries." #
# # # # #             }

# # # # #             self.send_response(200)
# # # # #             self.send_header('Content-type', 'application/json')
# # # # #             self.end_headers()
# # # # #             self.wfile.write(json.dumps(response_message).encode())

# # # # #         except Exception as e:
# # # # #             self.send_response(500)
# # # # #             self.end_headers()
# # # # #             self.wfile.write(str(e).encode())


# # # # # # import requests
# # # # # # import json

# # # # # # # Your Vercel App URL
# # # # # # # VERCEL_APP_URL = "https://your-project-name.vercel.app"
# # # # # # VERCEL_APP_URL = 'https://afas-email.vercel.app/''

# # # # # # def generate_approval_email(employee_id, employee_name, hours_count):
# # # # # #     """Creates the content for the email with the unique approval link."""
# # # # # #     # This link points to your Vercel app, which then calls post_hours_for_employee.py
# # # # # #     approval_link = f"{VERCEL_APP_URL}/api/approve?user_id={employee_id}"
    
# # # # # #     subject = f"Action Required: Copy your hours for this week, {employee_name}?"
# # # # # #     body = f"""
# # # # # #     Hi {employee_name},
    
# # # # # #     We found {hours_count} hour entries from your previous week. 
# # # # # #     Would you like to copy these to the current week?
    
# # # # # #     Click the link below to authorize the copy:
# # # # # #     {approval_link}
    
# # # # # #     If you do nothing, no hours will be copied.
# # # # # #     """
# # # # # #     return subject, body

# # # # # # def process_and_notify_all():
# # # # # #     # 1. Use your bulk downloader logic
# # # # # #     # (Assuming download_all_hours() is imported from your other file)
# # # # # #     all_employee_data = download_all_hours() 
    
# # # # # #     for emp_id, hours in all_employee_data.items():
# # # # # #         # Get the name from the first record if available
# # # # # #         emp_name = hours[0].get('Naam', 'Colleague')
# # # # # #         count = len(hours)
        
# # # # # #         subject, content = generate_approval_email(emp_id, emp_name, count)
        
# # # # # #         # 2. Integration with your Email Provider (Example using a generic sender)
# # # # # #         print(f"📧 Sending email to {emp_name} ({emp_id}) for {count} hours...")
# # # # # #         # send_email(to=emp_email, subject=subject, body=content) 

# # # # # # if __name__ == "__main__":
# # # # # #     process_and_notify_all()
