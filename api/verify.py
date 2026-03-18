from http.server import BaseHTTPRequestHandler
import base64
import requests
import json
from datetime import datetime, timedelta

# --- CONFIGURATION ---
AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices/connectors"
GET_CONNECTOR = "Project_realization" # Common standard connector name

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Calculate the same Monday date
        today = datetime.now()
        monday_date = (today - timedelta(days=today.weekday())).strftime('%Y-%m-%d')

        # 2. Authentication
        token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
        headers = {'Authorization': f'AfasToken {token}'}
        
        # 3. Build Filter (Looking for Employee 1000994 on our specific Date)
        # Filters: skip=-1 (all), take=-1 (all)
        filter_url = f"{BASE_URL}/{GET_CONNECTOR}?filterfieldids=Employee&filtervalues=1000994&operatortypes=1"

        try:
            resp = requests.get(filter_url, headers=headers)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            if resp.status_code == 200:
                data = resp.json()
                # We filter the JSON locally to find our specific Monday
                entries = [row for row in data.get('rows', []) if row.get('Date') == monday_date]
                
                result_html = "<h2>🔍 Verification Results</h2>"
                if entries:
                    result_html += f"<p style='color:green;'>Found {len(entries)} entry/entries for {monday_date}!</p>"
                    result_html += f"<pre>{json.dumps(entries, indent=4)}</pre>"
                else:
                    result_html += f"<p style='color:orange;'>No entries found for {monday_date} yet. (It might still be in the 'Import' buffer)</p>"
            else:
                result_html = f"<h2>❌ Query Failed</h2><pre>{resp.text}</pre>"

            self.wfile.write(f"<html><body>{result_html}</body></html>".encode())

        except Exception as e:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())
          
