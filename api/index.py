import base64
import requests
from http.server import BaseHTTPRequestHandler

AFAS_TOKEN_XML = """<token><version>1</version><data>84096424308C40DE98332B354EAC1F08F3AAC830633E4E9890D255A41C153140</data></token>"""
BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        token_base64 = base64.b64encode(AFAS_TOKEN_XML.encode('utf-8')).decode('utf-8')
        headers = {'Authorization': f'AfasToken {token_base64}'}

        # TEST: We are just ASKING the server if it knows what PtRealization is.
        # This is a standard GET request that should always work if the connector exists.
        url = f"{BASE_URL}/metainfo/update/PtRealization"
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                result = "✅ <b>Metadata Found!</b> The server knows the connector, but won't let us POST to it."
            else:
                result = f"❌ <b>Still 404!</b> This confirms AFAS has not exposed 'PtRealization' to the REST service yet."
        except Exception as e:
            result = f"💥 Error: {str(e)}"

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(result.encode())

# import base64
# import requests
# import json
# from http.server import BaseHTTPRequestHandler

# # --- CONFIGURATION ---
# AFAS_TOKEN_XML = """<token><version>1</version><data>84096424308C40DE98332B354EAC1F08F3AAC830633E4E9890D255A41C153140</data></token>"""
# BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

# class handler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         token_base64 = base64.b64encode(AFAS_TOKEN_XML.encode('utf-8')).decode('utf-8')
#         headers = {
#             'Authorization': f'AfasToken {token_base64}',
#             'Content-Type': 'application/json'
#         }

#         # Restored the mandatory PtRealization/Element/Fields structure
#         payload = {
#             "PtRealization": {
#                 "Element": {
#                     "Fields": {
#                         "CreateDeclarations": True,
#                         "ApprovWorkflow": True,
#                         "GetPcIdAndPrId": True,
#                         "DaTi": "2026-03-31",
#                         "VaIt": "1",
#                         "ItCd": "01",
#                         "Qu": "8",
#                         "EmId": "1000994",
#                         "PrId": "",
#                         "StId": "",
#                         "Ap": True,
#                         "Pr": True,
#                         "StTi": "17:00:00",
#                         "EnTi": "17:30:00",
#                         "PcId": "105"
#                     }
#                 }
#             }
#         }

#         try:
#             # Using the lowercase URL as we discussed earlier
#             url = f"{BASE_URL}/update/ptrealization" 
#             response = requests.post(url, headers=headers, data=json.dumps(payload))
            
#             if response.status_code == 200:
#                 result = f"🎉 <b>Success!</b> Response: {response.text}"
#             else:
#                 result = f"❌ <b>Status {response.status_code}</b><br>AFAS says: {response.text}"

#         except Exception as e:
#             result = f"💥 <b>Python Error:</b> {str(e)}"

#         self.send_response(200)
#         self.send_header('Content-type', 'text/html; charset=utf-8')
#         self.end_headers()
#         self.wfile.write(f"<html><body style='font-family:sans-serif;padding:30px;'>{result}</body></html>".encode())

# # import base64
# # import requests
# # import json
# # from http.server import BaseHTTPRequestHandler

# # # --- CONFIGURATION ---
# # AFAS_TOKEN_XML = """<token><version>1</version><data>84096424308C40DE98332B354EAC1F08F3AAC830633E4E9890D255A41C153140</data></token>"""
# # BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

# # # Vercel looks for this 'handler' class specifically
# # class handler(BaseHTTPRequestHandler):
# #     def do_GET(self):
# #         token_base64 = base64.b64encode(AFAS_TOKEN_XML.encode('utf-8')).decode('utf-8')
# #         headers = {
# #             'Authorization': f'AfasToken {token_base64}',
# #             'Content-Type': 'application/json'
# #         }

# #         payload = {
# #             "PtRealization": {
# #                 "Element": {
# #                     "Fields": {
# #                         "CreateDeclarations": True,
# #                         "GetPcIdAndPrId": True,
# #                         "DaTi": "2026-02-20",
# #                         "VaIt": 1,
# #                         "ItCd": "01",
# #                         "QuAn": 8.0,
# #                         "EmId": "1000994",
# #                         "PrId": "105"
# #                     }
# #                 }
# #             }
# #         }

# #         try:
# #             url = f"{BASE_URL}/update/PtRealization"
# #             response = requests.post(url, headers=headers, data=json.dumps(payload))
            
# #             if response.status_code == 200:
# #                 result = f"🎉 <b>Success!</b> Response: {response.text}"
# #             else:
# #                 result = f"❌ <b>Status {response.status_code}</b><br>AFAS says: {response.text}"

# #         except Exception as e:
# #             result = f"💥 <b>Python Error:</b> {str(e)}"

# #         self.send_response(200)
# #         self.send_header('Content-type', 'text/html; charset=utf-8')
# #         self.end_headers()
# #         self.wfile.write(f"<html><body style='font-family:sans-serif;padding:30px;'>{result}</body></html>".encode())

# # # <!DOCTYPE html>
# # # <html lang="en">
# # # <head>
# # #     <meta charset="UTF-8">
# # #     <title>AFAS Hour Copier</title>
# # #     <style>
# # #         body { font-family: sans-serif; padding: 20px; background: #f4f7f6; }
# # #         .card { background: white; padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center; }
# # #         button { background: #0070f3; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; }
# # #         button:hover { background: #0051bb; }
# # #         .status { font-size: 0.9em; color: #666; }
# # #     </style>
# # # </head>
# # # <body>
# # #     <h1>🕒 Employee Hour Dashboard</h1>
# # #     <div id="dashboard">Loading data from AFAS...</div>

# # #     <script>
# # #         async function loadDashboard() {
# # #             try {
# # #                 // This calls your working Python script!
# # #                 const response = await fetch('/api/load_hour_data');
# # #                 const data = await response.json();
# # #                 const container = document.getElementById('dashboard');
# # #                 container.innerHTML = '';

# # #                 // Loop through the data we saw in the JSON earlier
# # #                 Object.keys(data).forEach(empId => {
# # #                     const emp = data[empId];
# # #                     const card = document.createElement('div');
# # #                     card.className = 'card';
# # #                     card.innerHTML = `
# # #                         <div>
# # #                             <strong>${emp.name}</strong> (ID: ${empId})<br>
# # #                             <span class="status">${emp.hours_to_copy.length} entries found</span>
# # #                         </div>
# # #                         <button onclick="copyHours('${empId}')">Copy to AFAS</button>
# # #                     `;
# # #                     container.appendChild(card);
# # #                 });
# # #             } catch (err) {
# # #                 document.getElementById('dashboard').innerText = 'Error loading data.';
# # #             }
# # #         }

# # #         async function copyHours(empId) {
# # #             alert('Triggering AFAS copy for Employee: ' + empId);
# # #             // This will eventually call your api/approve.py script
# # #             const resp = await fetch(`/api/approve?user_id=${empId}`);
# # #             const result = await resp.json();
# # #             alert(result.message || 'Action processed!');
# # #         }

# # #         loadDashboard();
# # #     </script>
# # # </body>
# # # </html>

# # # # from flask import Flask, request
# # # # import requests
# # # # import os
# # # # from itsdangerous import URLSafeTimedSerializer

# # # # app = Flask(__name__)

# # # # # Config from your script
# # # # SECRET_KEY = os.environ.get('SECRET_KEY', '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')
# # # # SECURITY_SALT = "copy-hours-v1"
# # # # serializer = URLSafeTimedSerializer(SECRET_KEY)

# # # # GITHUB_TOKEN = os.getenv("GH_PAT")
# # # # REPO_OWNER = "wy85-bit"
# # # # REPO_NAME = "Afas_email"

# # # # @app.route('/copy-hours')
# # # # def trigger_action():
# # # #     # 1. Grab the ID from the URL (either ?token= or ?user=)
# # # #     # This allows your manual tests to work!
# # # #     target_id = request.args.get('token') or request.args.get('user')
    
# # # #     if not target_id:
# # # #         return "<h1>❌ Error</h1><p>No user or token provided in the URL.</p>", 400

# # # #     try:
# # # #         # 2. Trigger GitHub Action
# # # #         url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/dispatches"
# # # #         headers = {
# # # #             "Authorization": f"token {GITHUB_TOKEN}",
# # # #             "Accept": "application/vnd.github.v3+json"
# # # #         }
# # # #         data = {
# # # #             "event_type": "copy_hours_trigger",
# # # #             "client_payload": {"user": target_id} 
# # # #         }
        
# # # #         # Send the request to GitHub
# # # #         resp = requests.post(url, headers=headers, json=data)
        
# # # #         if resp.status_code == 204:
# # # #             return f"<h1>✅ Sync Started</h1><p>GitHub is now copying hours for {target_id}!</p>"
# # # #         else:
# # # #             return f"<h1>❌ GitHub Error</h1><p>{resp.text}</p>", resp.status_code

# # # #     except Exception as e:
# # # #         # This only triggers if the code itself crashes
# # # #         return f"<h1>❌ Script Error</h1><p>{str(e)}</p>", 500




# # # # # from flask import Flask, request
# # # # # import requests
# # # # # import os

# # # # # app = Flask(__name__)

# # # # # # DO NOT paste the string here. Vercel will pull it from the 'Settings' tab.
# # # # # GITHUB_TOKEN = os.getenv("GH_PAT") 
# # # # # REPO_OWNER = "wy85-bit"
# # # # # REPO_NAME = "Afas_email"

# # # # # @app.route('/')
# # # # # def home():
# # # # #     return "Listener is active. Use /copy-hours?user=NAME to trigger."

# # # # # @app.route('/copy-hours')
# # # # # def trigger_action():
# # # # #     user_id = request.args.get('user')
    
# # # # #     if not user_id:
# # # # #         return "Error: No user specified", 400

# # # # #     if not GITHUB_TOKEN:
# # # # #         return "Error: GH_PAT environment variable not found on Vercel", 500

# # # # #     url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/dispatches"
    
# # # # #     headers = {
# # # # #         # Changed 'Bearer' to 'token'
# # # # #         "Authorization": f"token {GITHUB_TOKEN}",
# # # # #         "Accept": "application/vnd.github.v3+json"
# # # # #     }
    
# # # # #     data = {
# # # # #         "event_type": "copy_hours_trigger",
# # # # #         "client_payload": {"user": user_id}
# # # # #     }

# # # # #     response = requests.post(url, headers=headers, json=data)
    
# # # # #     if response.status_code == 204:
# # # # #         return f"<h1>Success!</h1><p>Action triggered for {user_id}.</p>"
# # # # #     else:
# # # # #         # This will help us see if it's STILL a credential error or something else
# # # # #         return f"GitHub API Error ({response.status_code}): {response.text}", 500






