from http.server import BaseHTTPRequestHandler
import base64
import requests
import json

# --- CONFIGURATION ---
API_KEY = "5BA4B542D3654105BCDB197D8FE4A23C"
ENV_KEY = "E4E4E336283D4A69891CA03BE85D4A57"
BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

def get_afas_headers():
    # This is the EXACT string you just gave me
    raw_token = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
    
    # We must encode the WHOLE XML string into Base64
    encoded_token = base64.b64encode(raw_token.encode('utf-8')).decode('utf-8')
    
    return {
        'Authorization': f'AfasToken {encoded_token}',
        'Content-Type': 'application/json'
    }
    
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        headers = get_afas_headers()
        url = f"{BASE_URL}/connectors/Profit_Realization"
        
        try:
            response = requests.get(url, headers=headers)
            
            # SUCCESS PATH
            if response.status_code == 200:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response.json()).encode())
            
            # ERROR PATH - Let's see the details!
            else:
                self.send_response(200) # Sending 200 so the browser shows the error clearly
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                # We extract the full text from AFAS here
                error_info = {
                    "status_code": response.status_code,
                    "afas_raw_error": response.text, 
                    "used_url": url
                }
                self.wfile.write(json.dumps(error_info).encode())

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
