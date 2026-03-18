from http.server import BaseHTTPRequestHandler
import base64
import requests
import json
from datetime import datetime, timedelta

# --- CONFIGURATION ---
AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices/connectors"
GET_CONNECTOR = "Profit_Realization" 

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Setup Authentication
        token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
        headers = {'Authorization': f'AfasToken {token}'}
        
        # 2. Get the last 50 entries
        # We use ?take=50 to see the most recent data
        url = f"{BASE_URL}/{GET_CONNECTOR}?take=50"

        try:
            resp = requests.get(url, headers=headers)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            if resp.status_code == 200:
                data = resp.json()
                rows = data.get('rows', [])
                
                # We filter for your ID (1000994)
                # Note: We check for 'Medewerker' as that's the common AFAS name
                matches = [r for r in rows if str(r.get('Medewerker')) == "1000994" or str(r.get('Employee')) == "1000994"]
                
                html = "<html><body style='font-family: sans-serif; padding: 20px;'>"
                html += "<h1>🔍 Verification Result</h1>"
                
                if matches:
                    html += "<h2 style='color:green;'>🎉 Success! I found your entries.</h2>"
                    html += f"<pre style='background:#f4f4f4; padding:10px;'>{json.dumps(matches, indent=4)}</pre>"
                else:
                    html += "<h2 style='color:orange;'>⚠️ No exact match for 1000994 yet.</h2>"
                    html += "<p>This might be because the field name is different. Check the 'Raw Sample' below:</p>"
                    html += "<h3>Raw Sample (First 2 entries found):</h3>"
                    html += f"<pre style='background:#eee; padding:10px;'>{json.dumps(rows[:2], indent=4)}</pre>"
                
                html += "</body></html>"
            else:
                html = f"<h2>❌ AFAS Error {resp.status_code}</h2><pre>{resp.text}</pre>"

            self.wfile.write(html.encode('utf-8'))

        except Exception as e:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"Script Error: {str(e)}".encode())

# from http.server import BaseHTTPRequestHandler
# import base64
# import requests

# AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"

# class handler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
#         headers = {'Authorization': f'AfasToken {token}'}
#         url = "https://90114.resttest.afas.online/ProfitRestServices/metainfo/get"
        
#         try:
#             resp = requests.get(url, headers=headers)
#             self.send_response(200)
#             self.send_header('Content-type', 'application/json')
#             self.end_headers()
#             self.wfile.write(resp.text.encode())
#         except Exception as e:
#             self.send_response(200)
#             self.end_headers()
#             self.wfile.write(f"Discovery Error: {str(e)}".encode())
