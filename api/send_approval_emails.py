import requests
import json

# Your Vercel App URL
VERCEL_APP_URL = "https://your-project-name.vercel.app"

def generate_approval_email(employee_id, employee_name, hours_count):
    """Creates the content for the email with the unique approval link."""
    # This link points to your Vercel app, which then calls post_hours_for_employee.py
    approval_link = f"{VERCEL_APP_URL}/api/approve?user_id={employee_id}"
    
    subject = f"Action Required: Copy your hours for this week, {employee_name}?"
    body = f"""
    Hi {employee_name},
    
    We found {hours_count} hour entries from your previous week. 
    Would you like to copy these to the current week?
    
    Click the link below to authorize the copy:
    {approval_link}
    
    If you do nothing, no hours will be copied.
    """
    return subject, body

def process_and_notify_all():
    # 1. Use your bulk downloader logic
    # (Assuming download_all_hours() is imported from your other file)
    all_employee_data = download_all_hours() 
    
    for emp_id, hours in all_employee_data.items():
        # Get the name from the first record if available
        emp_name = hours[0].get('Naam', 'Colleague')
        count = len(hours)
        
        subject, content = generate_approval_email(emp_id, emp_name, count)
        
        # 2. Integration with your Email Provider (Example using a generic sender)
        print(f"📧 Sending email to {emp_name} ({emp_id}) for {count} hours...")
        # send_email(to=emp_email, subject=subject, body=content) 

if __name__ == "__main__":
    process_and_notify_all()
