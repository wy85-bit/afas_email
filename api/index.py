from flask import Flask, request
import requests
import os
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)

# Config from your script
SECRET_KEY = os.environ.get('SECRET_KEY', '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')
SECURITY_SALT = "copy-hours-v1"
serializer = URLSafeTimedSerializer(SECRET_KEY)

GITHUB_TOKEN = os.getenv("GH_PAT")
REPO_OWNER = "wy85-bit"
REPO_NAME = "Afas_email"

@app.route('/copy-hours')
def trigger_action():
    token = request.args.get('token')
    try:
        # Decrypt the token to get the real Employee ID
        user_id = serializer.loads(token, salt=SECURITY_SALT, max_age=604800)
        
        # Trigger GitHub Action
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/dispatches"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "event_type": "copy_hours_trigger",
            "client_payload": {"user": user_id} 
        }
        
        requests.post(url, headers=headers, json=data)
        return "<h1>✅ Sync Started</h1><p>GitHub is now copying your hours!</p>"
    except Exception as e:
        return f"<h1>❌ Link Expired or Invalid</h1>", 403





# from flask import Flask, request
# import requests
# import os

# app = Flask(__name__)

# # DO NOT paste the string here. Vercel will pull it from the 'Settings' tab.
# GITHUB_TOKEN = os.getenv("GH_PAT") 
# REPO_OWNER = "wy85-bit"
# REPO_NAME = "Afas_email"

# @app.route('/')
# def home():
#     return "Listener is active. Use /copy-hours?user=NAME to trigger."

# @app.route('/copy-hours')
# def trigger_action():
#     user_id = request.args.get('user')
    
#     if not user_id:
#         return "Error: No user specified", 400

#     if not GITHUB_TOKEN:
#         return "Error: GH_PAT environment variable not found on Vercel", 500

#     url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/dispatches"
    
#     headers = {
#         # Changed 'Bearer' to 'token'
#         "Authorization": f"token {GITHUB_TOKEN}",
#         "Accept": "application/vnd.github.v3+json"
#     }
    
#     data = {
#         "event_type": "copy_hours_trigger",
#         "client_payload": {"user": user_id}
#     }

#     response = requests.post(url, headers=headers, json=data)
    
#     if response.status_code == 204:
#         return f"<h1>Success!</h1><p>Action triggered for {user_id}.</p>"
#     else:
#         # This will help us see if it's STILL a credential error or something else
#         return f"GitHub API Error ({response.status_code}): {response.text}", 500

