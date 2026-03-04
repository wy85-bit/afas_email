from http.server import BaseHTTPRequestHandler
import base64
import requests
import json

# --- CONFIGURATION ---
API_KEY = "5BA4B542D3654105BCDB197D8FE4A23C"
ENV_KEY = "E4E4E336283D4A69891CA03BE85D4A57"
BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

def get_afas_headers():
    """Constructs the Base64 token header that AFAS requires."""
    raw_token = f"<token>{API_KEY}{ENV_KEY}</token>"
    encoded_token = base64.b64encode(raw_token.encode('utf-8')).decode('utf-8')
    return {
        'Authorization': f'AfasToken {encoded_token}',
        'Content-Type': 'application/json'
    }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """This function triggers when you visit the URL in your browser."""
        headers = get_afas_headers()
        url = f"{BASE_URL}/connectors/Profit_Realization"
        
        try:
            # 1. Call AFAS
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                rows = data.get('rows', [])
                
                # 2. Group the data by Employee
                grouped_data = {}
                for row in rows:
                    emp_id = row.get('Medewerker')
                    if emp_id not in grouped_data:
                        grouped_data[emp_id] = {
                            "name": row.get('Naam', 'Unknown'),
                            "email": row.get('Email', None),
                            "hours_to_copy": []
                        }
                    grouped_data[emp_id]["hours_to_copy"].append({
                        "project": row.get('Project'),
                        "description": row.get('Toelichting'),
                        "units": row.get('Aantal')
                    })
                
                # 3. Send successful response to browser
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(grouped_data).encode())
            
            else:
                # Handle AFAS errors (like 401 Unauthorized)
                self.send_response(response.status_code)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                error_msg = {"error": "AFAS Error", "details": response.text}
                self.wfile.write(json.dumps(error_msg).encode())

        except Exception as e:
            # Handle Python crashes
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
