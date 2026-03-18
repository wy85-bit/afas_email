from http.server import BaseHTTPRequestHandler
import base64
import requests

AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
        headers = {'Authorization': f'AfasToken {token}'}
        url = "https://90114.resttest.afas.online/ProfitRestServices/metainfo/get"
        
        try:
            resp = requests.get(url, headers=headers)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(resp.text.encode())
        except Exception as e:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"Discovery Error: {str(e)}".encode())
