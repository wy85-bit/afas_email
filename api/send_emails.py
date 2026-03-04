from http.server import BaseHTTPRequestHandler
import json
import requests

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # --- SAFETY SETTINGS ---
        MY_PRIVATE_EMAIL = "winnie.yap@veneficus.nl" # <--- PUT YOUR EMAIL HERE!
        
        # In a real run, we'd loop through all 50 people.
        # For this test, we are only sending ONE email to YOU.
        
        try:
            # This simulates the email logic
            subject = "Vercel Test: AFAS Hour Update"
            body = "Hi Winnie, the connection to environment 90114 is working!"
            
            # Here you would plug in your Email Service (like SendGrid or Mailgun)
            # For now, we'll just return a success message to the browser.
            
            response_message = {
                "status": "Safety Mode Active",
                "recipient": MY_PRIVATE_EMAIL,
                "message": "If an email service was connected, it would have sent now!",
                "test_data_sample": "Employee 1000077 has entries." #
            }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_message).encode())

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())


# import requests
# import json

# # Your Vercel App URL
# # VERCEL_APP_URL = "https://your-project-name.vercel.app"
# VERCEL_APP_URL = 'https://afas-email.vercel.app/''

# def generate_approval_email(employee_id, employee_name, hours_count):
#     """Creates the content for the email with the unique approval link."""
#     # This link points to your Vercel app, which then calls post_hours_for_employee.py
#     approval_link = f"{VERCEL_APP_URL}/api/approve?user_id={employee_id}"
    
#     subject = f"Action Required: Copy your hours for this week, {employee_name}?"
#     body = f"""
#     Hi {employee_name},
    
#     We found {hours_count} hour entries from your previous week. 
#     Would you like to copy these to the current week?
    
#     Click the link below to authorize the copy:
#     {approval_link}
    
#     If you do nothing, no hours will be copied.
#     """
#     return subject, body

# def process_and_notify_all():
#     # 1. Use your bulk downloader logic
#     # (Assuming download_all_hours() is imported from your other file)
#     all_employee_data = download_all_hours() 
    
#     for emp_id, hours in all_employee_data.items():
#         # Get the name from the first record if available
#         emp_name = hours[0].get('Naam', 'Colleague')
#         count = len(hours)
        
#         subject, content = generate_approval_email(emp_id, emp_name, count)
        
#         # 2. Integration with your Email Provider (Example using a generic sender)
#         print(f"📧 Sending email to {emp_name} ({emp_id}) for {count} hours...")
#         # send_email(to=emp_email, subject=subject, body=content) 

# if __name__ == "__main__":
#     process_and_notify_all()
