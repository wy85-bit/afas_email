from flask import Flask, request
import requests
import os

app = Flask(__name__)

# DO NOT paste the string here. Vercel will pull it from the 'Settings' tab.
GITHUB_TOKEN = os.getenv("GH_PAT") 
REPO_OWNER = "wy85-bit"
REPO_NAME = "Afas_email"

@app.route('/')
def home():
    return "Listener is active. Use /copy-hours?user=NAME to trigger."

@app.route('/copy-hours')
def trigger_action():
    user_id = request.args.get('user')
    
    if not user_id:
        return "Error: No user specified", 400

    if not GITHUB_TOKEN:
        return "Error: GH_PAT environment variable not found on Vercel", 500

    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/dispatches"
    
    headers = {
        # Changed 'Bearer' to 'token'
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "event_type": "copy_hours_trigger",
        "client_payload": {"user": user_id}
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 204:
        return f"<h1>Success!</h1><p>Action triggered for {user_id}.</p>"
    else:
        # This will help us see if it's STILL a credential error or something else
        return f"GitHub API Error ({response.status_code}): {response.text}", 500
