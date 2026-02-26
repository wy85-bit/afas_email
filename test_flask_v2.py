from flask import Flask, request
import requests
import os

app = Flask(__name__)

# You'll need a GitHub Personal Access Token (PAT) with 'repo' scope
GITHUB_TOKEN = os.getenv("GH_PAT")
REPO_OWNER = "wy85-bit"
REPO_NAME = "Afas_email"

@app.route('/copy-hours')
def trigger_action():
    user_id = request.args.get('user')
    
    if not user_id:
        return "Error: No user specified", 400

    # This is the "Repository Dispatch" API call
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/dispatches"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    data = {
        "event_type": "copy_hours_trigger", # Matches the 'types' in your YAML
        "client_payload": {"user": user_id}  # Passes the username to the Action
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 204:
        return f"<h1>Success!</h1><p>Hours are being copied for {user_id}. You can close this tab.</p>"
    else:
        return f"Error: {response.text}", 500
