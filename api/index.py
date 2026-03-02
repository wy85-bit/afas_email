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
    # 1. Grab the ID from the URL (either ?token= or ?user=)
    # This allows your manual tests to work!
    target_id = request.args.get('token') or request.args.get('user')
    
    if not target_id:
        return "<h1>❌ Error</h1><p>No user or token provided in the URL.</p>", 400

    try:
        # 2. Trigger GitHub Action
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/dispatches"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "event_type": "copy_hours_trigger",
            "client_payload": {"user": target_id} 
        }
        
        # Send the request to GitHub
        resp = requests.post(url, headers=headers, json=data)
        
        if resp.status_code == 204:
            return f"<h1>✅ Sync Started</h1><p>GitHub is now copying hours for {target_id}!</p>"
        else:
            return f"<h1>❌ GitHub Error</h1><p>{resp.text}</p>", resp.status_code

    except Exception as e:
        # This only triggers if the code itself crashes
        return f"<h1>❌ Script Error</h1><p>{str(e)}</p>", 500




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





