import base64
import requests
import json
from http.server import BaseHTTPRequestHandler

# --- CONFIGURATION ---
AFAS_TOKEN_XML = """<token><version>1</version><data>84096424308C40DE98332B354EAC1F08F3AAC830633E4E9890D255A41C153140</data></token>"""
BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Prepare Authorization
        token_base64 = base64.b64encode(AFAS_TOKEN_XML.encode('utf-8')).decode('utf-8')
        headers = {
            'Authorization': f'AfasToken {token_base64}',
            'Content-Type': 'application/json'
        }

        # 2. Define the Payload (Cleanly Aligned)
        payload = {
            "PtRealization": {
                "Element": {
                    "Fields": {
                        "CreateDeclarations": True,
                        "GetPcIdAndPrId": True,
                        "DaTi": "2026-02-20",
                        "VaIt": "1",
                        "ItCd": "01",
                        "Qu": "8",
                        "EmId": "1000994",
                        "Ch": True,
                        "Ap": True,
                        "Pr": True,
                        "PcId": "105"
                    }
                }
            }
        }

        # 3. Execution Block
        try:
            url = f"{BASE_URL}/update/PtRealization"
            # We send the JSON data here
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            
            if response.status_code == 200:
                result = f"🎉 <b>Success!</b> Hours posted successfully.<br>Response: {response.text}"
            else:
                # Capturing the AFAS error message for better debugging
                result = f"❌ <b>Failed with status {response.status_code}</b><br>AFAS says: {response.text}"

        except Exception as e:
            result = f"💥 <b>Python Error:</b> {str(e)}"

        self._send_html(result)

    def _send_html(self, message):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(f"<html><body style='font-family:sans-serif;padding:30px;'>{message}</body></html>".encode())

# import base64
# import requests
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

#         # We will try the 3 most likely URL variations
#         urls = [
#             f"{BASE_URL}/update/PtRealization",    # Standard
#             f"{BASE_URL}/update/ptrealization",    # Lowercase
#             f"{BASE_URL}/update/PtRealizations"    # Plural
#         ]

#         results = "<h3>URL Connectivity Test</h3><ul>"

#         for url in urls:
#             try:
#                 # We send an empty request just to see if the URL "exists" (404 vs 400/500)
#                 resp = requests.post(url, headers=headers, json={})
#                 status = resp.status_code
                
#                 if status == 404:
#                     results += f"<li>❌ {url} -> <b>NOT FOUND (404)</b></li>"
#                 elif status == 401:
#                     results += f"<li>🔑 {url} -> <b>AUTH ERROR (401)</b></li>"
#                 else:
#                     # Anything other than 404 means the URL works!
#                     results += f"<li>✅ {url} -> <b>FOUND (Status {status})</b></li>"
#             except Exception as e:
#                 results += f"<li>💥 {url} -> Error: {str(e)}</li>"

#         results += "</ul>"
#         self._send_html(results)

#     def _send_html(self, message):
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html; charset=utf-8')
#         self.end_headers()
#         self.wfile.write(f"<html><body style='font-family:sans-serif;padding:30px;'>{message}</body></html>".encode())

# import base64
# import requests
# import json
# from http.server import BaseHTTPRequestHandler

# # --- CONFIGURATION ---
# AFAS_TOKEN_XML = """<token><version>1</version><data>84096424308C40DE98332B354EAC1F08F3AAC830633E4E9890D255A41C153140</data></token>"""
# BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

# class handler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         # 1. Prepare Authorization
#         token_base64 = base64.b64encode(AFAS_TOKEN_XML.encode('utf-8')).decode('utf-8')
#         headers = {
#             'Authorization': f'AfasToken {token_base64}',
#             'Content-Type': 'application/json'
#         }

#         # 2. Define the Payload using our NEW Metadata Keys
#         # Based on your image_e4e882.png:
#         # DaTi = Datum, VaIt = Type item, ItCd = Itemcode
#         payload = {
#             "PtRealization": {

#     "Element": {

#       "Fields": {

#         "CreateDeclarations": true,

#         "GetPcIdAndPrId": true,

#         "DaTi": "2026-02-20",

#         "VaIt": "1",

#         "ItCd": "01",

#         "Qu": "8",

#         "EmId": "1000994",

#         "Ch": true,

#         "Ap": true,

#         "Pr": true,

#         "PcId": "105"

 
#         }

#         try:
#             url = f"{BASE_URL}/update/PtRealization"
#             response = requests.post(url, headers=headers, data=json.dumps(payload))
            
#             if response.status_code == 200:
#                 result = f"🎉 <b>Success!</b> Hours posted successfully.<br>Response: {response.text}"
#             else:
#                 # If it still fails, the error message will now be more specific
#                 result = f"❌ <b>Failed with status {response.status_code}</b><br>AFAS says: {response.text}"

#         except Exception as e:
#             result = f"💥 <b>Python Error:</b> {str(e)}"

#         self._send_html(result)

#     def _send_html(self, message):
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html; charset=utf-8')
#         self.end_headers()
#         self.wfile.write(f"<html><body style='font-family:sans-serif;padding:30px;'>{message}</body></html>".encode())

# # from http.server import BaseHTTPRequestHandler
# # import base64
# # import requests
# # import json

# # # --- CONFIGURATION ---
# # AFAS_TOKEN_XML = """<token><version>1</version><data>84096424308C40DE98332B354EAC1F08F3AAC830633E4E9890D255A41C153140</data></token>"""
# # BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

# # class handler(BaseHTTPRequestHandler):
# #     def do_GET(self):
# #         token_base64 = base64.b64encode(AFAS_TOKEN_XML.encode('utf-8')).decode('utf-8')
# #         headers = {'Authorization': f'AfasToken {token_base64}', 'Content-Type': 'application/json'}

# #         try:
# #             # We are calling the 'describe' endpoint for the UpdateConnector
# #             url = f"{BASE_URL}/metainfo/update/PtRealization"
# #             resp = requests.get(url, headers=headers)
            
# #             if resp.status_code == 200:
# #                 meta = resp.json()
# #                 # Let's filter for just the mandatory fields to keep it readable
# #                 mandatory_fields = [
# #                     {"Field": f.get("fieldId"), "Label": f.get("label"), "Type": f.get("dataType")}
# #                     for f in meta.get("fields", []) if f.get("mandatory")
# #                 ]
                
# #                 res = "<h3>as Required Fields for PtRealization</h3>"
# #                 res += "<p>If our POST request is missing any of these, AFAS will reject it.</p>"
# #                 res += f"<pre style='background:#f4f4f4;padding:10px;'>{json.dumps(mandatory_fields, indent=2)}</pre>"
# #             else:
# #                 res = f"❌ <b>Metadata Error:</b> {resp.status_code}<br>Your admin might need to 'unblock' the UpdateConnector definition too."

# #         except Exception as e:
# #             res = f"💥 <b>Crashed:</b> {str(e)}"

# #         self._send_html(res)

# #     def _send_html(self, message):
# #         self.send_response(200)
# #         self.send_header('Content-type', 'text/html; charset=utf-8')
# #         self.end_headers()
# #         self.wfile.write(f"<html><body style='font-family:sans-serif;padding:30px;'>{message}</body></html>".encode())

# # # from http.server import BaseHTTPRequestHandler
# # # import base64
# # # import requests
# # # import json

# # # # --- CONFIGURATION ---
# # # AFAS_TOKEN_XML = """<token><version>1</version><data>84096424308C40DE98332B354EAC1F08F3AAC830633E4E9890D255A41C153140</data></token>"""
# # # BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

# # # class handler(BaseHTTPRequestHandler):
# # #     def do_GET(self):
# # #         token_base64 = base64.b64encode(AFAS_TOKEN_XML.encode('utf-8')).decode('utf-8')
# # #         headers = {'Authorization': f'AfasToken {token_base64}', 'Content-Type': 'application/json'}

# # #         # We are going to try the 'Global' connector we saw in your screenshot
# # #         try:
# # #             url = f"{BASE_URL}/connectors/ProfitEmployerRealization?take=1"
# # #             resp = requests.get(url, headers=headers)
            
# # #             if resp.status_code == 200:
# # #                 data = resp.json().get('rows', [])
# # #                 if data:
# # #                     res = "<h3>✅ BANANA FOUND! 🍌</h3><p>This connector works! Here is the data structure:</p>"
# # #                     res += f"<pre>{json.dumps(data[0], indent=2)}</pre>"
# # #                 else:
# # #                     res = "⚠️ This one is empty too. AFAS is really hiding these hours!"
# # #             else:
# # #                 res = f"❌ Error: {resp.status_code}. AFAS said: {resp.text}"

# # #         except Exception as e:
# # #             res = f"💥 Error: {str(e)}"

# # #         self._send_html(res)

# # #     def _send_html(self, message):
# # #         self.send_response(200)
# # #         self.send_header('Content-type', 'text/html; charset=utf-8')
# # #         self.end_headers()
# # #         self.wfile.write(f"<html><body style='font-family:sans-serif;padding:30px;'>{message}</body></html>".encode())


# # # # from http.server import BaseHTTPRequestHandler
# # # # import base64
# # # # import requests
# # # # import json

# # # # # --- CONFIGURATION ---
# # # # AFAS_TOKEN_XML = """<token><version>1</version><data>84096424308C40DE98332B354EAC1F08F3AAC830633E4E9890D255A41C153140</data></token>"""
# # # # BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

# # # # class handler(BaseHTTPRequestHandler):
# # # #     def do_GET(self):
# # # #         token_base64 = base64.b64encode(AFAS_TOKEN_XML.encode('utf-8')).decode('utf-8')
# # # #         headers = {
# # # #             'Authorization': f'AfasToken {token_base64}',
# # # #             'Content-Type': 'application/json'
# # # #         }

# # # #         try:
# # # #             # We ask for the 1 most recent entry to see the field structure
# # # #             # skip=-1 often gets the very last record in some AFAS versions, 
# # # #             # but we'll stick to take=1 for maximum compatibility.
# # # #             url = f"{BASE_URL}/connectors/Profit_Realization?take=1"
# # # #             resp = requests.get(url, headers=headers)
            
# # # #             if resp.status_code == 200:
# # # #                 data = resp.json().get('rows', [])
# # # #                 if data:
# # # #                     # Success! We found the map.
# # # #                     message = "<h3>✅ Blueprint Found!</h3><p>Copy this entire block and send it to Gemmy:</p>"
# # # #                     message += f"<pre style='background:#f4f4f4;padding:15px;'>{json.dumps(data[0], indent=2)}</pre>"
# # # #                 else:
# # # #                     message = "⚠️ <b>Connector found, but it's empty.</b><br>This usually means there's a 'Data Filter' on the App Connector blocking you from seeing records."
# # # #             else:
# # # #                 message = f"❌ <b>Error calling Connector:</b> {resp.status_code}<br>{resp.text}"

# # # #         except Exception as e:
# # # #             message = f"💥 <b>Script Error:</b> {str(e)}"

# # # #         self._send_html(message)

# # # #     def _send_html(self, message):
# # # #         self.send_response(200)
# # # #         self.send_header('Content-type', 'text/html; charset=utf-8')
# # # #         self.end_headers()
# # # #         self.wfile.write(f"<html><body style='font-family:sans-serif;padding:30px;line-height:1.6;'>{message}</body></html>".encode())
        
# # # # # from http.server import BaseHTTPRequestHandler
# # # # # import base64
# # # # # import requests
# # # # # import json

# # # # # # --- CONFIGURATION ---
# # # # # AFAS_TOKEN_XML = """<token><version>1</version><data>84096424308C40DE98332B354EAC1F08F3AAC830633E4E9890D255A41C153140</data></token>"""
# # # # # BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

# # # # # class handler(BaseHTTPRequestHandler):
# # # # #     def do_GET(self):
# # # # #         token_base64 = base64.b64encode(AFAS_TOKEN_XML.encode('utf-8')).decode('utf-8')
# # # # #         headers = {'Authorization': f'AfasToken {token_base64}', 'Content-Type': 'application/json'}

# # # # #         # We try three different 'buckets' to find any existing data
# # # # #         connectors = ["Profit_Realization", "Actual_costing", "Project_entries"]
        
# # # # #         output = "<h2>🔍 Blueprint Finder</h2><p>Searching for a working example in your system...</p>"

# # # # #         for conn in connectors:
# # # # #             try:
# # # # #                 # We ask for the 1 most recent entry from ANYONE to see the fields
# # # # #                 url = f"{BASE_URL}/connectors/{conn}?take=1"
# # # # #                 resp = requests.get(url, headers=headers)
                
# # # # #                 if resp.status_code == 200:
# # # # #                     data = resp.json().get('rows', [])
# # # # #                     if data:
# # # # #                         output += f"<h3>✅ Found data in: {conn}</h3>"
# # # # #                         output += f"<pre>{json.dumps(data[0], indent=2)}</pre>"
# # # # #                         break # Stop once we find a blueprint
# # # # #                     else:
# # # # #                         output += f"⚠️ {conn} returned 0 rows.<br>"
# # # # #                 else:
# # # # #                     output += f"❌ {conn} error: {resp.status_code}<br>"
# # # # #             except Exception as e:
# # # # #                 output += f"💥 {conn} crashed: {str(e)}<br>"

# # # # #         if "✅" not in output:
# # # # #             output += "<br><b>Conclusion:</b> Your API token is blind. It has no permission to read any hour tables."

# # # # #         self._send_html(output)

# # # # #     def _send_html(self, message):
# # # # #         self.send_response(200)
# # # # #         self.send_header('Content-type', 'text/html; charset=utf-8')
# # # # #         self.end_headers()
# # # # #         self.wfile.write(f"<html><body style='font-family:sans-serif;padding:30px;'>{message}</body></html>".encode())


# # # # # # from http.server import BaseHTTPRequestHandler
# # # # # # import base64
# # # # # # import requests
# # # # # # import json

# # # # # # # --- CONFIGURATION ---
# # # # # # AFAS_TOKEN_XML = """<token><version>1</version><data>84096424308C40DE98332B354EAC1F08F3AAC830633E4E9890D255A41C153140</data></token>"""
# # # # # # BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"
# # # # # # # Using the ID from your previous notes
# # # # # # EMPLOYEE_ID = "1000994" 
# # # # # # # Based on your latest screenshot image_7357ea.png
# # # # # # CONNECTOR_NAME = "Profit_Employees" 

# # # # # # class handler(BaseHTTPRequestHandler):
# # # # # #     def do_GET(self):
# # # # # #         token_base64 = base64.b64encode(AFAS_TOKEN_XML.encode('utf-8')).decode('utf-8')
# # # # # #         headers = {
# # # # # #             'Authorization': f'AfasToken {token_base64}',
# # # # # #             'Content-Type': 'application/json'
# # # # # #         }

# # # # # #         # List of potential internal field names for the Employee ID
# # # # # #         possible_fields = ["EmployeeId", "Employee", "Medewerker"]
# # # # # #         found_data = None
# # # # # #         last_error = ""

# # # # # #         try:
# # # # # #             # Loop through potential field names until we find a match
# # # # # #             for field in possible_fields:
# # # # # #                 url = (f"{BASE_URL}/connectors/{CONNECTOR_NAME}?"
# # # # # #                        f"filterfieldids={field}&"
# # # # # #                        f"filtervalues={EMPLOYEE_ID}&"
# # # # # #                        f"operatortypes=1&take=1")
                
# # # # # #                 resp = requests.get(url, headers=headers)
                
# # # # # #                 if resp.status_code == 200:
# # # # # #                     rows = resp.json().get('rows', [])
# # # # # #                     if rows:
# # # # # #                         found_data = rows[0]
# # # # # #                         break
# # # # # #                 else:
# # # # # #                     last_error = f"API Error {resp.status_code}: {resp.text}"

# # # # # #             # --- RESPONSE HANDLING ---
# # # # # #             if found_data:
# # # # # #                 self._send_html(f"""
# # # # # #                     <h2 style='color:#2e7d32;'>✅ Connection Successful!</h2>
# # # # # #                     <p>I found your record in <b>{CONNECTOR_NAME}</b>.</p>
# # # # # #                     <div style='background:#f4f4f4; padding:15px; border-radius:5px; border-left:5px solid #2e7d32;'>
# # # # # #                         <b>Field matched:</b> {field}<br>
# # # # # #                         <b>Data retrieved:</b>
# # # # # #                         <pre>{json.dumps(found_data, indent=2)}</pre>
# # # # # #                     </div>
# # # # # #                 """)
# # # # # #             else:
# # # # # #                 self._send_html(f"""
# # # # # #                     <h2 style='color:#d32f2f;'>❌ No Data Found</h2>
# # # # # #                     <p>I reached the server, but couldn't find ID <b>{EMPLOYEE_ID}</b> in <b>{CONNECTOR_NAME}</b>.</p>
# # # # # #                     <p style='font-size:0.9em; color:#666;'><i>Technical Details: {last_error if last_error else "Search returned 0 rows for all common field names."}</i></p>
# # # # # #                     <hr>
# # # # # #                     <b>Next Steps:</b>
# # # # # #                     <ul>
# # # # # #                         <li>Ensure the Employee ID '{EMPLOYEE_ID}' exists in AFAS.</li>
# # # # # #                         <li>Check if the App Connector has permissions for '{CONNECTOR_NAME}'.</li>
# # # # # #                     </ul>
# # # # # #                 """)

# # # # # #         except Exception as e:
# # # # # #             self._send_html(f"<h2 style='color:#d32f2f;'>❌ Script Error</h2><p>{str(e)}</p>")

# # # # # #     def _send_html(self, message):
# # # # # #         self.send_response(200)
# # # # # #         self.send_header('Content-type', 'text/html; charset=utf-8')
# # # # # #         self.end_headers()
# # # # # #         html = f"""
# # # # # #         <html>
# # # # # #             <body style='font-family:sans-serif; padding:30px; line-height:1.6; background:#fafafa;'>
# # # # # #                 <div style='max-width:700px; margin:auto; background:white; padding:30px; border-radius:12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
# # # # # #                     {message}
# # # # # #                 </div>
# # # # # #             </body>
# # # # # #         </html>
# # # # # #         """
# # # # # #         self.wfile.write(html.encode())


# # # # # # # from http.server import BaseHTTPRequestHandler
# # # # # # # import base64
# # # # # # # import requests
# # # # # # # import json
# # # # # # # from datetime import datetime, timedelta

# # # # # # # # --- CONFIGURATION ---
# # # # # # # AFAS_TOKEN_XML = """<token><version>1</version><data>84096424308C40DE98332B354EAC1F08F3AAC830633E4E9890D255A41C153140</data></token>"""
# # # # # # # BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"
# # # # # # # EMPLOYEE_ID = "1000994"

# # # # # # # class handler(BaseHTTPRequestHandler):
# # # # # # #     def do_GET(self):
# # # # # # #         token_base64 = base64.b64encode(AFAS_TOKEN_XML.encode('utf-8')).decode('utf-8')
# # # # # # #         headers = {
# # # # # # #             'Authorization': f'AfasToken {token_base64}',
# # # # # # #             'Content-Type': 'application/json'
# # # # # # #         }

# # # # # # #         # 1. Calculate Date Ranges
# # # # # # #         today = datetime.now()
# # # # # # #         # Get this Monday
# # # # # # #         this_monday = today - timedelta(days=today.weekday())
# # # # # # #         this_friday = this_monday + timedelta(days=4)
        
# # # # # # #         # Get last week's Monday and Friday to use as a template
# # # # # # #         last_monday = this_monday - timedelta(days=7)
# # # # # # #         last_friday = last_monday + timedelta(days=4)

# # # # # # #         source_start = last_monday.strftime('%Y-%m-%d')
# # # # # # #         source_end = last_friday.strftime('%Y-%m-%d')

# # # # # # #         try:
# # # # # # #             # 2. FETCH SOURCE: Get all hours from last week
# # # # # # #             # Filter: Employee AND Date Range (>= last_monday AND <= last_friday)
# # # # # # #             get_url = (f"{BASE_URL}/connectors/Profit_Realization?"
# # # # # # #                        f"filterfieldids=EmployeeId,Datum,Datum&"
# # # # # # #                        f"filtervalues={EMPLOYEE_ID},{source_start},{source_end}&"
# # # # # # #                        f"operatortypes=1,4,6") # 1=Equal, 4=Greater/Equal, 6=Less/Equal
            
# # # # # # #             get_resp = requests.get(get_url, headers=headers)
# # # # # # #             source_rows = get_resp.json().get('rows', [])

# # # # # # #             if not source_rows:
# # # # # # #                 self._send_html(f"⚠️ No hours found to copy from last week ({source_start} to {source_end}).")
# # # # # # #                 return

# # # # # # #             # 3. POST ENTRIES: Loop through last week's hours
# # # # # # #             success_count = 0
# # # # # # #             error_count = 0

# # # # # # #             for entry in source_rows:
# # # # # # #                 # Calculate the new date (Original Date + 7 days)
# # # # # # #                 orig_date = datetime.strptime(entry['Datum'], '%Y-%m-%dT%H:%M:%S')
# # # # # # #                 new_date = (orig_date + timedelta(days=7)).strftime('%Y-%m-%d')

# # # # # # #                 # SAFETY CHECK: Skip if this specific entry already exists for the new date
# # # # # # #                 # (Simple check: skip if date is already populated for this employee)
# # # # # # #                 check_url = f"{BASE_URL}/connectors/Profit_Realization?filterfieldids=EmployeeId,Datum&filtervalues={EMPLOYEE_ID},{new_date}&operatortypes=1,1"
# # # # # # #                 if len(requests.get(check_url, headers=headers).json().get('rows', [])) > 0:
# # # # # # #                     continue

# # # # # # #                 payload = {
# # # # # # #                     "PtRealization": {
# # # # # # #                         "Element": {
# # # # # # #                             "EnId": EMPLOYEE_ID,
# # # # # # #                             "PrId": str(entry.get("Projectnummer", "")),
# # # # # # #                             "Da": new_date,
# # # # # # #                             "Qu": float(entry.get("Aantal_eenheden", 0)),
# # # # # # #                             "ItId": str(entry.get("Itemcode", "")),
# # # # # # #                             "UnId": str(entry.get("Eenheid", "UUR")),
# # # # # # #                             "De": f"Auto-Copy: {entry.get('Omschrijving', 'Hours')}"
# # # # # # #                         }
# # # # # # #                     }
# # # # # # #                 }

# # # # # # #                 post_url = f"{BASE_URL}/updateconnectors/PtRealization"
# # # # # # #                 post_resp = requests.post(post_url, headers=headers, data=json.dumps(payload))
                
# # # # # # #                 if post_resp.status_code in [200, 201]:
# # # # # # #                     success_count += 1
# # # # # # #                 else:
# # # # # # #                     error_count += 1

# # # # # # #             self._send_html(f"✅ <b>Processing Complete:</b><br>"
# # # # # # #                             f"- {success_count} entries copied to this week.<br>"
# # # # # # #                             f"- {error_count} errors occurred.<br>"
# # # # # # #                             f"- Skipped existing entries automatically.")

# # # # # # #         except Exception as e:
# # # # # # #             self._send_html(f"❌ <b>Script Error:</b> {str(e)}")

# # # # # # #     def _send_html(self, message):
# # # # # # #         self.send_response(200)
# # # # # # #         self.send_header('Content-type', 'text/html; charset=utf-8')
# # # # # # #         self.end_headers()
# # # # # # #         self.wfile.write(f"<html><body style='font-family:sans-serif; padding:20px;'><h2>{message}</h2></body></html>".encode())


# # # # # # # # from http.server import BaseHTTPRequestHandler
# # # # # # # # import base64
# # # # # # # # import requests
# # # # # # # # import json
# # # # # # # # from datetime import datetime

# # # # # # # # # --- CONFIGURATION ---
# # # # # # # # # Paste your FULL XML <token> block here
# # # # # # # # AFAS_TOKEN_XML = """<token><version>1</version><data>84096424308C40DE98332B354EAC1F08F3AAC830633E4E9890D255A41C153140</data></token>"""
# # # # # # # # BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

# # # # # # # # class handler(BaseHTTPRequestHandler):
# # # # # # # #     def do_GET(self):
# # # # # # # #         # 1. Prepare Authorization
# # # # # # # #         token_base64 = base64.b64encode(AFAS_TOKEN_XML.encode('utf-8')).decode('utf-8')
# # # # # # # #         headers = {
# # # # # # # #             'Authorization': f'AfasToken {token_base64}',
# # # # # # # #             'Content-Type': 'application/json'
# # # # # # # #         }
        
# # # # # # # #         today_str = datetime.now().strftime('%Y-%m-%d')

# # # # # # # #         try:
# # # # # # # #             # 2. SAFETY CHECK: Search if hours already exist for today
# # # # # # # #             # We filter by Employee (1000994) AND Date (today)
# # # # # # # #             check_url = f"{BASE_URL}/connectors/Profit_Realization?filterfieldids=EmployeeId,Datum&filtervalues=1000994,{today_str}&operatortypes=1,1"
# # # # # # # #             check_resp = requests.get(check_url, headers=headers)
            
# # # # # # # #             if check_resp.status_code == 200:
# # # # # # # #                 existing_rows = check_resp.json().get('rows', [])
# # # # # # # #                 if len(existing_rows) > 0:
# # # # # # # #                     self._send_html(f"🛑 <b>Safety Stop:</b> You already have {len(existing_rows)} entries for {today_str}. Script blocked to prevent duplicates!")
# # # # # # # #                     return
            
# # # # # # # #             # 3. FETCH TEMPLATE: Get the most recent hour to copy
# # # # # # # #             get_url = f"{BASE_URL}/connectors/Profit_Realization?filterfieldids=EmployeeId&filtervalues=1000994&operatortypes=1&take=1"
# # # # # # # #             get_resp = requests.get(get_url, headers=headers)
# # # # # # # #             rows = get_resp.json().get('rows', [])
            
# # # # # # # #             if not rows:
# # # # # # # #                 self._send_html("⚠️ No source hours found in your history to copy.")
# # # # # # # #                 return

# # # # # # # #             source = rows[0]
            
# # # # # # # #             # 4. CREATE PAYLOAD
# # # # # # # #             payload = {
# # # # # # # #                 "PtRealization": {
# # # # # # # #                     "Element": {
# # # # # # # #                         "EnId": "1000994",
# # # # # # # #                         "PrId": str(source.get("Projectnummer", "")),
# # # # # # # #                         "Da": today_str,
# # # # # # # #                         "Qu": float(source.get("Aantal_eenheden", 8.0)), # Default to 8 if not found
# # # # # # # #                         "ItId": str(source.get("Itemcode", "")),
# # # # # # # #                         "UnId": str(source.get("Eenheid", "UUR")),
# # # # # # # #                         "De": f"Auto-Copy: {source.get('Omschrijving', 'Hours')}"
# # # # # # # #                     }
# # # # # # # #                 }
# # # # # # # #             }

# # # # # # # #             # 5. POST TO AFAS
# # # # # # # #             post_url = f"{BASE_URL}/updateconnectors/PtRealization"
# # # # # # # #             post_resp = requests.post(post_url, headers=headers, data=json.dumps(payload))
            
# # # # # # # #             if post_resp.status_code in [200, 201]:
# # # # # # # #                 self._send_html(f"✅ <b>Success!</b> Hours copied for {today_str}. Go have a coffee!")
# # # # # # # #             else:
# # # # # # # #                 self._send_html(f"❌ <b>AFAS Error {post_resp.status_code}:</b> {post_resp.text}")

# # # # # # # #         except Exception as e:
# # # # # # # #             self._send_html(f"❌ <b>Script Error:</b> {str(e)}")

# # # # # # # #     def _send_html(self, message):
# # # # # # # #         self.send_response(200)
# # # # # # # #         self.send_header('Content-type', 'text/html; charset=utf-8')
# # # # # # # #         self.end_headers()
# # # # # # # #         self.wfile.write(f"<html><body style='font-family:sans-serif; padding:20px;'><h2>{message}</h2></body></html>".encode())

# # # # # # # # # from http.server import BaseHTTPRequestHandler
# # # # # # # # # import base64
# # # # # # # # # import requests
# # # # # # # # # import json
# # # # # # # # # from datetime import datetime

# # # # # # # # # # --- CONFIGURATION ---
# # # # # # # # # AFAS_TOKEN_XML = "<token><version>1</version><data>84096424308C40DE98332B354EAC1F08F3AAC830633E4E9890D255A41C153140</data></token>"
# # # # # # # # # # Use .resttest for your T90114TE environment
# # # # # # # # # BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

# # # # # # # # # class handler(BaseHTTPRequestHandler):
# # # # # # # # #     def do_GET(self):
# # # # # # # # #         token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
# # # # # # # # #         headers = {
# # # # # # # # #             'Authorization': f'AfasToken {token}',
# # # # # # # # #             'Content-Type': 'application/json'
# # # # # # # # #         }
        
# # # # # # # # #         # 1. Fetch template record
# # # # # # # # #         get_url = f"{BASE_URL}/connectors/Profit_Realization?filterfieldids=EmployeeId&filtervalues=1000994&operatortypes=1&take=1"

# # # # # # # # #         try:
# # # # # # # # #             get_resp = requests.get(get_url, headers=headers)
# # # # # # # # #             # rows = get_resp.json().get('rows', [])
# # # # # # # # #             if get_resp.status_code != 200:
# # # # # # # # #                 self._send_html(f"❌ Error from AFAS: {get_resp.status_code} - {get_resp.text}")
# # # # # # # # #                 return
# # # # # # # # #             try:
# # # # # # # # #                 rows = get_resp.json().get('rows', [])
# # # # # # # # #             except Exception:
# # # # # # # # #                 self._send_html(f"❌ AFAS sent a non-JSON response: {get_resp.text}")
# # # # # # # # #                 return
# # # # # # # # #             if not rows:
# # # # # # # # #                 self._send_html("⚠️ No source hours found to copy.")
# # # # # # # # #                 return

# # # # # # # # #             source = rows[0]
# # # # # # # # #             # AFAS standard date format (YYYY-MM-DD)
# # # # # # # # #             today_str = datetime.now().strftime('%Y-%m-%d')
            
# # # # # # # # #             # 2. THE REFINED PAYLOAD (Strict AFAS Field Mapping)
# # # # # # # # #             payload = {
# # # # # # # # #                 "PtRealization": {
# # # # # # # # #                     "Element": {
# # # # # # # # #                         "EnId": "1000994",                                  # Employee (Medewerker)
# # # # # # # # #                         "PrId": str(source.get("Projectnummer", "")),       # Project ID
# # # # # # # # #                         "Da": today_str,                                    # Date
# # # # # # # # #                         "Qu": float(source.get("Aantal_eenheden", 0)),      # Quantity
# # # # # # # # #                         "ItId": str(source.get("Itemcode", "")),            # Item/Work Type
# # # # # # # # #                         "UnId": str(source.get("Eenheid", "UUR")),          # Unit
# # # # # # # # #                         "De": f"Copy: {source.get('Omschrijving', 'Hours')}" # Description
# # # # # # # # #                     }
# # # # # # # # #                 }
# # # # # # # # #             }

# # # # # # # # #             # 3. THE CORRECT ENDPOINT
# # # # # # # # #             post_url = f"{BASE_URL}/updateconnectors/PtRealization"
            
# # # # # # # # #             post_resp = requests.post(
# # # # # # # # #                 post_url, 
# # # # # # # # #                 headers=headers, 
# # # # # # # # #                 data=json.dumps(payload)
# # # # # # # # #             )
            
# # # # # # # # #             # Capture the response text for debugging
# # # # # # # # #             response_text = post_resp.text if post_resp.text else "[Empty Response]"

# # # # # # # # #             if post_resp.status_code in [200, 201]:
# # # # # # # # #                 # AFAS returns the record ID in 'results' or 'id'
# # # # # # # # #                 new_id = post_resp.json().get('results', {}).get('PtRealization', {}).get('id', 'Created')
# # # # # # # # #                 self._send_html(f"✅ Success! Created record for {today_str}.")
# # # # # # # # #             else:
# # # # # # # # #                 # This will tell us EXACTLY what field is wrong
# # # # # # # # #                 self._send_html(f"❌ AFAS Error {post_resp.status_code}: <pre>{response_text}</pre>")

# # # # # # # # #         except Exception as e:
# # # # # # # # #             self._send_html(f"❌ Script Error: {str(e)}")

# # # # # # # # #     def _send_html(self, message):
# # # # # # # # #         self.send_response(200)
# # # # # # # # #         self.send_header('Content-type', 'text/html; charset=utf-8')
# # # # # # # # #         self.end_headers()
# # # # # # # # #         self.wfile.write(f"<html><body><h2>{message}</h2></body></html>".encode())

# # # # # # # # # # from http.server import BaseHTTPRequestHandler
# # # # # # # # # # import base64
# # # # # # # # # # import requests
# # # # # # # # # # import json
# # # # # # # # # # from datetime import datetime

# # # # # # # # # # # --- CONFIGURATION ---
# # # # # # # # # # AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
# # # # # # # # # # BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

# # # # # # # # # # class handler(BaseHTTPRequestHandler):
# # # # # # # # # #     def do_GET(self):
# # # # # # # # # #         token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
# # # # # # # # # #         headers = {
# # # # # # # # # #             'Authorization': f'AfasToken {token}',
# # # # # # # # # #             'Content-Type': 'application/json'
# # # # # # # # # #         }
        
# # # # # # # # # #         # 1. Fetch template record (We know this works!)
# # # # # # # # # #         get_url = f"{BASE_URL}/connectors/Profit_Realization?filterfieldids=EmployeeId&filtervalues=1000994&operatortypes=1&take=1"

# # # # # # # # # #         try:
# # # # # # # # # #             get_resp = requests.get(get_url, headers=headers)
# # # # # # # # # #             if get_resp.status_code != 200:
# # # # # # # # # #                 self._send_html(f"❌ GET Error: {get_resp.status_code}")
# # # # # # # # # #                 return

# # # # # # # # # #             rows = get_resp.json().get('rows', [])
# # # # # # # # # #             if not rows:
# # # # # # # # # #                 self._send_html("⚠️ No source hours found to copy.")
# # # # # # # # # #                 return

# # # # # # # # # #             source = rows[0]
# # # # # # # # # #             today_str = datetime.now().strftime('%Y-%m-%dT00:00:00Z')
            
# # # # # # # # # #            # 2. THE REFINED PAYLOAD: PtRealization (Nacalculatie)
# # # # # # # # # #            # 2. THE REFINED PAYLOAD: PtRealization (Nacalculatie)
# # # # # # # # # #             # 2. THE REFINED PAYLOAD: PtRealization (Nacalculatie)
# # # # # # # # # #             # Note: AFAS uses EnId for Employee (Medewerker) and ItId for Item (Itemcode)
# # # # # # # # # #             payload = {
# # # # # # # # # #                 "PtRealization": {
# # # # # # # # # #                     "Element": {
# # # # # # # # # #                         "EnId": "1000994",                                 # Medewerker ID (Standard is EnId)
# # # # # # # # # #                         "PrId": str(source.get("Projectnummer") or source.get("PrId")), # Projectnummer
# # # # # # # # # #                         "Da": datetime.now().strftime('%Y-%m-%dT00:00:00'),# Date (Remove the 'Z' if AFAS throws a format error)
# # # # # # # # # #                         "Qu": float(source.get("Aantal_eenheden") or source.get("Qu") or 0), # Aantal eenheden
# # # # # # # # # #                         "UnId": str(source.get("Eenheid") or "UUR"),       # Eenheid
# # # # # # # # # #                         "ItId": str(source.get("Itemcode") or ""),         # Itemcode (Mandatory in most AFAS configs)
# # # # # # # # # #                         "De": f"Copy: {source.get('Omschrijving', 'Hours')}" # Omschrijving
# # # # # # # # # #                     }
# # # # # # # # # #                 }
# # # # # # # # # #             }

# # # # # # # # # #             # 3. THE CORRECT ENDPOINT
# # # # # # # # # #             # Ensure no underscores and correct casing
# # # # # # # # # #             post_url = f"{BASE_URL}/updateconnectors/PtRealization"
            
# # # # # # # # # #             post_resp = requests.post(
# # # # # # # # # #                 post_url, 
# # # # # # # # # #                 headers=headers, 
# # # # # # # # # #                 data=json.dumps(payload)
# # # # # # # # # #             )
            
# # # # # # # # # #             if post_resp.status_code in [200, 201]:
# # # # # # # # # #                 new_id = post_resp.json().get('id', 'unknown')
# # # # # # # # # #                 self._send_html(f"✅ Success! Created record {new_id} for {today_str}.")
# # # # # # # # # #             else:
# # # # # # # # # #                 # This prints the error to your Terminal/Command Prompt
# # # # # # # # # #                 print(f"DEBUG: AFAS Response Body -> {post_resp.text}")     
# # # # # # # # # #                 # This sends the error to your Browser
# # # # # # # # # #                 self._send_html(f"❌ AFAS Error {post_resp.status_code}: {repr(post_resp.text)}")
# # # # # # # # # #         except Exception as e:
# # # # # # # # # #             self._send_html(f"Script Error: {str(e)}")
                
# # # # # # # # # #     def _send_html(self, message):
# # # # # # # # # #         self.send_response(200)
# # # # # # # # # #         self.send_header('Content-type', 'text/html; charset=utf-8')
# # # # # # # # # #         self.end_headers()
# # # # # # # # # #         self.wfile.write(f"<html><body><h2>{message}</h2></body></html>".encode())
            
# # # # # # # # # # # from http.server import BaseHTTPRequestHandler
# # # # # # # # # # # import base64
# # # # # # # # # # # import requests
# # # # # # # # # # # import json
# # # # # # # # # # # from datetime import datetime

# # # # # # # # # # # # --- CONFIGURATION ---
# # # # # # # # # # # AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
# # # # # # # # # # # BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

# # # # # # # # # # # class handler(BaseHTTPRequestHandler):
# # # # # # # # # # #     def do_GET(self):
# # # # # # # # # # #         token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
# # # # # # # # # # #         headers = {
# # # # # # # # # # #             'Authorization': f'AfasToken {token}',
# # # # # # # # # # #             'Content-Type': 'application/json'
# # # # # # # # # # #         }
        
# # # # # # # # # # #         # 1. Get the template row (This part we know works!)
# # # # # # # # # # #         get_url = f"{BASE_URL}/connectors/Profit_Realization?filterfieldids=EmployeeId&filtervalues=1000994&operatortypes=1&take=1"

# # # # # # # # # # #         try:
# # # # # # # # # # #             get_resp = requests.get(get_url, headers=headers)
            
# # # # # # # # # # #             if get_resp.status_code == 200:
# # # # # # # # # # #                 rows = get_resp.json().get('rows', [])
# # # # # # # # # # #                 if not rows:
# # # # # # # # # # #                     res_text = "No source hours found for 1000994 to copy."
# # # # # # # # # # #                 else:
# # # # # # # # # # #                     source = rows[0]
# # # # # # # # # # #                     # We'll use today as the destination date
# # # # # # # # # # #                     today_str = datetime.now().strftime('%Y-%m-%dT00:00:00Z')
                    
# # # # # # # # # # #                     # 2. Refined Payload for PtRealization
# # # # # # # # # # #                     # We use 'EmId' and 'PrId' which are common for AFAS Updates
# # # # # # # # # # #                     payload = {
# # # # # # # # # # #                         "PtRealization": {
# # # # # # # # # # #                             "Element": {
# # # # # # # # # # #                                 "Fields": {
# # # # # # # # # # #                                     "EmId": "1000994",
# # # # # # # # # # #                                     "PrId": source.get("ProjectId"),
# # # # # # # # # # #                                     "Da": today_str,
# # # # # # # # # # #                                     "Qu": source.get("QuantityUnit"),
# # # # # # # # # # #                                     "Uu": "UUR",
# # # # # # # # # # #                                     "De": f"Auto-copy from {source.get('DateTime')}"
# # # # # # # # # # #                                 }
# # # # # # # # # # #                             }
# # # # # # # # # # #                         }
# # # # # # # # # # #                     }

# # # # # # # # # # #                     # 3. Try the Update with the standard URL pattern
# # # # # # # # # # #                     post_url = f"{BASE_URL}/updateconnectors/PtRealization"
# # # # # # # # # # #                     post_resp = requests.post(post_url, headers=headers, data=json.dumps(payload))
                    
# # # # # # # # # # #                     if post_resp.status_code in [200, 201]:
# # # # # # # # # # #                         res_text = f"✅ Success! Copied {source.get('QuantityUnit')} hours to {today_str}."
# # # # # # # # # # #                     else:
# # # # # # # # # # #                         # This gives us the real reason for the 404 or other errors
# # # # # # # # # # #                         res_text = f"❌ AFAS Update Error {post_resp.status_code}: {post_resp.text}"
# # # # # # # # # # #             else:
# # # # # # # # # # #                 res_text = f"❌ Error fetching template: {get_resp.status_code}"

# # # # # # # # # # #             self.send_response(200)
# # # # # # # # # # #             self.send_header('Content-type', 'text/html; charset=utf-8')
# # # # # # # # # # #             self.end_headers()
# # # # # # # # # # #             self.wfile.write(f"<html><body><h2>{res_text}</h2></body></html>".encode())

# # # # # # # # # # #         except Exception as e:
# # # # # # # # # # #             self.send_response(200)
# # # # # # # # # # #             self.end_headers()
# # # # # # # # # # #             self.wfile.write(f"Critical Script Error: {str(e)}".encode())

# # # # # # # # # # # # from http.server import BaseHTTPRequestHandler
# # # # # # # # # # # # import base64
# # # # # # # # # # # # import requests
# # # # # # # # # # # # import json
# # # # # # # # # # # # from datetime import datetime

# # # # # # # # # # # # # --- CONFIGURATION ---
# # # # # # # # # # # # AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
# # # # # # # # # # # # BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"
# # # # # # # # # # # # GET_PATH = "connectors/Profit_Realization"
# # # # # # # # # # # # # Fixed the casing here to match AFAS standards
# # # # # # # # # # # # UPDATE_PATH = "updateconnectors/PtRealization"

# # # # # # # # # # # # class handler(BaseHTTPRequestHandler):
# # # # # # # # # # # #     def do_GET(self):
# # # # # # # # # # # #         token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
# # # # # # # # # # # #         headers = {
# # # # # # # # # # # #             'Authorization': f'AfasToken {token}',
# # # # # # # # # # # #             'Content-Type': 'application/json'
# # # # # # # # # # # #         }
        
# # # # # # # # # # # #         # 1. Fetch the latest entry for 1000994 to use as a template
# # # # # # # # # # # #         filter_url = f"{BASE_URL}/{GET_PATH}?filterfieldids=EmployeeId&filtervalues=1000994&operatortypes=1&take=1"

# # # # # # # # # # # #         try:
# # # # # # # # # # # #             get_resp = requests.get(filter_url, headers=headers)
            
# # # # # # # # # # # #             if get_resp.status_code == 200:
# # # # # # # # # # # #                 rows = get_resp.json().get('rows', [])
# # # # # # # # # # # #                 if not rows:
# # # # # # # # # # # #                     res_text = "No source hours found for 1000994."
# # # # # # # # # # # #                 else:
# # # # # # # # # # # #                     source = rows[0]
# # # # # # # # # # # #                     # Use today's date
# # # # # # # # # # # #                     new_date = datetime.now().strftime('%Y-%m-%dT00:00:00Z')
                    
# # # # # # # # # # # #                     # 2. Refined Payload with correct AFAS Update Codes
# # # # # # # # # # # #                     payload = {
# # # # # # # # # # # #                         "PtRealization": {
# # # # # # # # # # # #                             "Element": {
# # # # # # # # # # # #                                 "Fields": {
# # # # # # # # # # # #                                     "EmId": "1000994",
# # # # # # # # # # # #                                     "PrId": source.get("ProjectId"),
# # # # # # # # # # # #                                     "Da": new_date,
# # # # # # # # # # # #                                     "Qu": source.get("QuantityUnit"),
# # # # # # # # # # # #                                     "Uu": "UUR", # Added mandatory Unit ID
# # # # # # # # # # # #                                     "De": f"Auto-copy: {source.get('Description')}"
# # # # # # # # # # # #                                 }
# # # # # # # # # # # #                             }
# # # # # # # # # # # #                         }
# # # # # # # # # # # #                     }

# # # # # # # # # # # #                     # 3. POST to AFAS
# # # # # # # # # # # #                     post_url = f"{BASE_URL}/{UPDATE_PATH}"
# # # # # # # # # # # #                     post_resp = requests.post(post_url, headers=headers, data=json.dumps(payload))
                    
# # # # # # # # # # # #                     if post_resp.status_code in [200, 201]:
# # # # # # # # # # # #                         res_text = f"✅ Success! Copied {source.get('QuantityUnit')} hours to {new_date}."
# # # # # # # # # # # #                     else:
# # # # # # # # # # # #                         # This will help us if there's a validation error (like 'Project not active')
# # # # # # # # # # # #                         res_text = f"❌ AFAS Update Error {post_resp.status_code}: {post_resp.text}"
# # # # # # # # # # # #             else:
# # # # # # # # # # # #                 res_text = f"❌ Error fetching data: {get_resp.status_code}"

# # # # # # # # # # # #             self.send_response(200)
# # # # # # # # # # # #             self.send_header('Content-type', 'text/html; charset=utf-8')
# # # # # # # # # # # #             self.end_headers()
# # # # # # # # # # # #             self.wfile.write(f"<h3>{res_text}</h3>".encode())

# # # # # # # # # # # #         except Exception as e:
# # # # # # # # # # # #             self.send_response(200)
# # # # # # # # # # # #             self.end_headers()
# # # # # # # # # # # #             self.wfile.write(f"Script Error: {str(e)}".encode())
            
# # # # # # # # # # # # # from http.server import BaseHTTPRequestHandler
# # # # # # # # # # # # # import base64
# # # # # # # # # # # # # import requests
# # # # # # # # # # # # # import json
# # # # # # # # # # # # # from datetime import datetime, timedelta

# # # # # # # # # # # # # # --- CONFIGURATION ---
# # # # # # # # # # # # # AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
# # # # # # # # # # # # # BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"
# # # # # # # # # # # # # # We read from the GetConnector and write to the UpdateConnector
# # # # # # # # # # # # # GET_CONNECTOR = "connectors/Profit_Realization"
# # # # # # # # # # # # # UPDATE_CONNECTOR = "updateconnectors/PtRealization"

# # # # # # # # # # # # # class handler(BaseHTTPRequestHandler):
# # # # # # # # # # # # #     def do_GET(self):
# # # # # # # # # # # # #         token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
# # # # # # # # # # # # #         headers = {
# # # # # # # # # # # # #             'Authorization': f'AfasToken {token}',
# # # # # # # # # # # # #             'Content-Type': 'application/json'
# # # # # # # # # # # # #         }
        
# # # # # # # # # # # # #         # 1. We filter specifically for your ID like we did in the verify script
# # # # # # # # # # # # #         filter_url = f"{BASE_URL}/{GET_CONNECTOR}?filterfieldids=EmployeeId&filtervalues=1000994&operatortypes=1&take=1"

# # # # # # # # # # # # #         try:
# # # # # # # # # # # # #             # Fetch the most recent entry to use as a template
# # # # # # # # # # # # #             get_resp = requests.get(filter_url, headers=headers)
            
# # # # # # # # # # # # #             if get_resp.status_code == 200:
# # # # # # # # # # # # #                 rows = get_resp.json().get('rows', [])
# # # # # # # # # # # # #                 if not rows:
# # # # # # # # # # # # #                     res_text = "No source hours found to copy."
# # # # # # # # # # # # #                 else:
# # # # # # # # # # # # #                     source = rows[0]
# # # # # # # # # # # # #                     # 2. Prepare the new entry (e.g., copying to TODAY)
# # # # # # # # # # # # #                     new_date = datetime.now().strftime('%Y-%m-%dT00:00:00Z')
                    
# # # # # # # # # # # # #                     payload = {
# # # # # # # # # # # # #                         "PtRealization": {
# # # # # # # # # # # # #                             "Element": {
# # # # # # # # # # # # #                                 "Fields": {
# # # # # # # # # # # # #                                     "EmId": source.get("EmployeeId"),
# # # # # # # # # # # # #                                     "PrId": source.get("ProjectId"),
# # # # # # # # # # # # #                                     "Da": new_date,
# # # # # # # # # # # # #                                     "Qu": source.get("QuantityUnit"),
# # # # # # # # # # # # #                                     "De": f"Copied: {source.get('Description')}"
# # # # # # # # # # # # #                                 }
# # # # # # # # # # # # #                             }
# # # # # # # # # # # # #                         }
# # # # # # # # # # # # #                     }

# # # # # # # # # # # # #                     # 3. POST the new data back to AFAS
# # # # # # # # # # # # #                     post_url = f"{BASE_URL}/{UPDATE_CONNECTOR}"
# # # # # # # # # # # # #                     post_resp = requests.post(post_url, headers=headers, data=json.dumps(payload))
                    
# # # # # # # # # # # # #                     # if post_resp.status_code in [200, 201]:
# # # # # # # # # # # # #                     #     res_text = f"Successfully copied {source.get('QuantityUnit')} hours to {new_date}!"
# # # # # # # # # # # # #                     # else:
# # # # # # # # # # # # #                     #     res_text = f"Failed to copy. AFAS says: {post_resp.text}"
                    
# # # # # # # # # # # # #                     # Updated error catching to see the actual AFAS message
# # # # # # # # # # # # #                     if post_resp.status_code in [200, 201]:
# # # # # # # # # # # # #                         res_text = f"Successfully copied {source.get('QuantityUnit')} hours!"
# # # # # # # # # # # # #                     else:
# # # # # # # # # # # # #                         # This will show us the EXACT field that is missing or wrong
# # # # # # # # # # # # #                         res_text = f"Failed. AFAS Error {post_resp.status_code}: {post_resp.text}"
# # # # # # # # # # # # #             else:
# # # # # # # # # # # # #                 res_text = f"Error fetching source data: {get_resp.status_code}"

# # # # # # # # # # # # #             self.send_response(200)
# # # # # # # # # # # # #             self.send_header('Content-type', 'text/plain')
# # # # # # # # # # # # #             self.end_headers()
# # # # # # # # # # # # #             self.wfile.write(res_text.encode())

# # # # # # # # # # # # #         except Exception as e:
# # # # # # # # # # # # #             self.send_response(500)
# # # # # # # # # # # # #             self.end_headers()
# # # # # # # # # # # # #             self.wfile.write(f"Server Error: {str(e)}".encode())

# # # # # # # # # # # # # # import base64
# # # # # # # # # # # # # # import requests
# # # # # # # # # # # # # # import json
# # # # # # # # # # # # # # from datetime import datetime, timedelta

# # # # # # # # # # # # # # # --- CONFIGURATION ---
# # # # # # # # # # # # # # # These keys are taken directly from your TestWinnie App Connector
# # # # # # # # # # # # # # API_KEY = "5BA4B542D3654105BCDB197D8FE4A23C"
# # # # # # # # # # # # # # ENV_KEY = "E4E4E336283D4A69891CA03BE85D4A57"
# # # # # # # # # # # # # # AFAS_URL = "https://90114.resttest.afas.online/ProfitRestServices" # Environment 90114

# # # # # # # # # # # # # # def get_afas_token():
# # # # # # # # # # # # # #     """
# # # # # # # # # # # # # #     Since we generated a specific user token, we use it directly.
# # # # # # # # # # # # # #     Paste the long string you copied from the AFAS wizard below.
# # # # # # # # # # # # # #     """
# # # # # # # # # # # # # #     # Replace the text inside the quotes with the new token you just copied
# # # # # # # # # # # # # #     new_user_token = "<token><version>1</version><data>935A787C2E884574974A3BA1DB4AC80470653AD4DDAD46DB9DF8092D1BA19D1D</data></token>"
    
# # # # # # # # # # # # # #     # We still need to Base64 encode it for the header
# # # # # # # # # # # # # #     raw_token = f"<token>{new_user_token}</token>"
# # # # # # # # # # # # # #     encoded_token = base64.b64encode(raw_token.encode('utf-8')).decode('utf-8')
# # # # # # # # # # # # # #     return encoded_token

# # # # # # # # # # # # # # def sync_hours(user_id):
# # # # # # # # # # # # # #     print(f"🚀 Starting sync for User ID: {user_id}")
    
# # # # # # # # # # # # # #     token = get_afas_token()
# # # # # # # # # # # # # #     headers = {
# # # # # # # # # # # # # #         'Authorization': f'AfasToken {token}',
# # # # # # # # # # # # # #         'Content-Type': 'application/json'
# # # # # # # # # # # # # #     }

# # # # # # # # # # # # # #     # Example: Fetching from the Profit_Realization GetConnector
# # # # # # # # # # # # # #     endpoint = f"{AFAS_URL}/connectors/Profit_Realization"
    
# # # # # # # # # # # # # #     try:
# # # # # # # # # # # # # #         response = requests.get(endpoint, headers=headers)
        
# # # # # # # # # # # # # #         if response.status_code == 200:
# # # # # # # # # # # # # #             print("✅ Success! Connected to AFAS.")
# # # # # # # # # # # # # #             data = response.json()
# # # # # # # # # # # # # #             # Here you would add your logic to process the hours
# # # # # # # # # # # # # #             print(f"Retrieved {len(data.get('rows', []))} records.")
# # # # # # # # # # # # # #         elif response.status_code == 401:
# # # # # # # # # # # # # #             print("❌ AFAS Connection Failed (401): Unauthorized.")
# # # # # # # # # # # # # #             print("Check: Is IP-restricties empty? Is user 90114 still in group PR-006?")
# # # # # # # # # # # # # #         else:
# # # # # # # # # # # # # #             print(f"❌ Failed with status code: {response.status_code}")
# # # # # # # # # # # # # #             print(f"Response: {response.text}")

# # # # # # # # # # # # # #     except Exception as e:
# # # # # # # # # # # # # #         print(f"⚠️ An error occurred: {e}")

# # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # #     # Using the ID from your user properties
# # # # # # # # # # # # # #     sync_hours("90114")

# # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # import sys
# # # # # # # # # # # # # # # import requests
# # # # # # # # # # # # # # # from datetime import datetime, timedelta
# # # # # # # # # # # # # # # import base64

# # # # # # # # # # # # # # # # --- CONFIG ---
# # # # # # # # # # # # # # # # Pulling the token from GitHub Secrets
# # # # # # # # # # # # # # # AFAS_TOKEN = os.getenv("AFAS_TOKEN")
# # # # # # # # # # # # # # # AFAS_BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

# # # # # # # # # # # # # # # def sync_hours(user_id):
# # # # # # # # # # # # # # #     """Copies hours for a specific user from last week to the current week."""
    
# # # # # # # # # # # # # # #     # 1. AUTHENTICATION (The Base64 "Secret Knock")
# # # # # # # # # # # # # # #     # We combine the API Key and Environment Key with a colon
# # # # # # # # # # # # # # #     # Based on your screenshot: 5BA4... : E4E4...
# # # # # # # # # # # # # # #     # 1. AUTHENTICATION (The "Double-Wrapped" Method)
# # # # # # # # # # # # # # #     # We combine the keys with a colon, wrap them in <token> tags, THEN encode.
# # # # # # # # # # # # # # #     import base64
    
# # # # # # # # # # # # # # #     # Your actual keys from the screenshot
# # # # # # # # # # # # # # #     api_key = "5BA4B542D3654105BCDB197D8FE4A23C"
# # # # # # # # # # # # # # #     env_key = "E4E4E336283D4A69891CA03BE85D4A57"

# # # # # # # # # # # # # # #     # Method: Combined with a colon and wrapped in the <token> tag
# # # # # # # # # # # # # # #     # This is the "Industry Standard" for AFAS REST services
# # # # # # # # # # # # # # #     token_content = f"<token>{api_key}{env_key}</token>"

# # # # # # # # # # # # # # #     # Encode to Base64
# # # # # # # # # # # # # # #     token_bytes = token_content.encode('utf-8')
# # # # # # # # # # # # # # #     encoded_token = base64.b64encode(token_bytes).decode('utf-8')

# # # # # # # # # # # # # # #     # The Header - Ensure there is exactly one space after 'AfasToken'
# # # # # # # # # # # # # # #     headers = {
# # # # # # # # # # # # # # #     'Authorization': f'AfasToken {encoded_token}',
# # # # # # # # # # # # # # #     'Content-Type': 'application/json'
# # # # # # # # # # # # # # #     }

# # # # # # # # # # # # # # #     try:
# # # # # # # # # # # # # # #         # 2. Calculate Date Range
# # # # # # # # # # # # # # #         today = datetime.now()
# # # # # # # # # # # # # # #         last_mon = (today - timedelta(days=today.weekday() + 7)).strftime('%Y-%m-%d')
# # # # # # # # # # # # # # #         last_sun = (today - timedelta(days=today.weekday() + 1)).strftime('%Y-%m-%d')

# # # # # # # # # # # # # # #         print(f"🚀 Starting sync for User ID: {user_id}")
# # # # # # # # # # # # # # #         print(f"📅 Last week was: {last_mon} to {last_sun}")
# # # # # # # # # # # # # # #         print(f"🔐 Auth: Sending Base64 encoded token...")

# # # # # # # # # # # # # # #         # 3. Fetch last week's entries
# # # # # # # # # # # # # # #         get_url = (
# # # # # # # # # # # # # # #             f"{AFAS_BASE_URL}/connectors/Profit_Realization"
# # # # # # # # # # # # # # #             f"?filterfieldids=EmployeeId,DateTime"
# # # # # # # # # # # # # # #             f"&filtervalues={user_id},{last_mon};{last_sun}"
# # # # # # # # # # # # # # #             f"&operatortypes=1,9"
# # # # # # # # # # # # # # #         )
        
# # # # # # # # # # # # # # #         response = requests.get(get_url, headers=headers)

# # # # # # # # # # # # # # #         if response.status_code != 200:
# # # # # # # # # # # # # # #             print(f"❌ AFAS Connection Failed ({response.status_code})")
# # # # # # # # # # # # # # #             print(f"Response Body: {response.text}")
# # # # # # # # # # # # # # #             return

# # # # # # # # # # # # # # #         source_data = response.json().get('rows', [])

# # # # # # # # # # # # # # #         if not source_data:
# # # # # # # # # # # # # # #             print(f"ℹ️ No hours found for {user_id} in the target range.")
# # # # # # # # # # # # # # #             return

# # # # # # # # # # # # # # #         print(f"✅ Found {len(source_data)} entries. Beginning copy...")

# # # # # # # # # # # # # # #         # 4. Post entries to the current week
# # # # # # # # # # # # # # #         success_count = 0
# # # # # # # # # # # # # # #         for entry in source_data:
# # # # # # # # # # # # # # #             original_date = datetime.strptime(entry['Da'], '%Y-%m-%d')
# # # # # # # # # # # # # # #             new_date = (original_date + timedelta(days=7)).strftime('%Y-%m-%d')
            
# # # # # # # # # # # # # # #             payload = {
# # # # # # # # # # # # # # #                 "PtRealization": {
# # # # # # # # # # # # # # #                     "Element": {
# # # # # # # # # # # # # # #                         "Fields": {
# # # # # # # # # # # # # # #                             "DaTi": new_date,
# # # # # # # # # # # # # # #                             "EmId": user_id,
# # # # # # # # # # # # # # #                             "PrId": entry.get('PrId', '82'),
# # # # # # # # # # # # # # #                             "StTi": entry.get('StTi', '09:00:00'),
# # # # # # # # # # # # # # #                             "EnTi": entry.get('EnTi', '17:00:00'),
# # # # # # # # # # # # # # #                             "Ap": True,
# # # # # # # # # # # # # # #                             "Pr": True
# # # # # # # # # # # # # # #                         }
# # # # # # # # # # # # # # #                     }
# # # # # # # # # # # # # # #                 }
# # # # # # # # # # # # # # #             }
            
# # # # # # # # # # # # # # #             post_res = requests.post(
# # # # # # # # # # # # # # #                 f"{AFAS_BASE_URL}/connectors/PtRealization", 
# # # # # # # # # # # # # # #                 json=payload, 
# # # # # # # # # # # # # # #                 headers=headers
# # # # # # # # # # # # # # #             )
            
# # # # # # # # # # # # # # #             if post_res.status_code in [200, 201, 204]:
# # # # # # # # # # # # # # #                 print(f"✔️ Copied: {entry.get('PrId', 'Work')} on {new_date}")
# # # # # # # # # # # # # # #                 success_count += 1
# # # # # # # # # # # # # # #             else:
# # # # # # # # # # # # # # #                 print(f"⚠️ Failed to copy entry for {new_date}: {post_res.text}")

# # # # # # # # # # # # # # #         print(f"🎉 Done! Successfully synced {success_count} entries.")

# # # # # # # # # # # # # # #     except Exception as e:
# # # # # # # # # # # # # # #         print(f"❌ Script Error: {e}")

# # # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # # #     if len(sys.argv) > 2 and sys.argv[1] == '--user':
# # # # # # # # # # # # # # #         target_user = sys.argv[2]
# # # # # # # # # # # # # # #         sync_hours(target_user)
# # # # # # # # # # # # # # #     else:
# # # # # # # # # # # # # # #         print("❌ Error: No User ID provided.")

# # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # import sys
# # # # # # # # # # # # # # # # import requests
# # # # # # # # # # # # # # # # from datetime import datetime, timedelta
# # # # # # # # # # # # # # # # import base64

# # # # # # # # # # # # # # # # # --- CONFIG ---
# # # # # # # # # # # # # # # # AFAS_TOKEN = os.getenv("AFAS_TOKEN")
# # # # # # # # # # # # # # # # AFAS_BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

# # # # # # # # # # # # # # # # def sync_hours(user_id):
# # # # # # # # # # # # # # # #     """Copies hours for a specific user from last week to the current week."""
    
# # # # # # # # # # # # # # # #     # if not AFAS_TOKEN:
# # # # # # # # # # # # # # # #     #     print("❌ Error: AFAS_TOKEN environment variable is missing in GitHub Secrets!")
# # # # # # # # # # # # # # # #     #     return

# # # # # # # # # # # # # # # #     # Using the specific combined format with a colon
# # # # # # # # # # # # # # # #     # headers = {
# # # # # # # # # # # # # # # #     #     'Authorization': f'AfasToken <token>5BA4B542D3654105BCDB197D8FE4A23C:E4E4E336283D4A69891CA03BE85D4A57</token>',
# # # # # # # # # # # # # # # #     #     'Content-Type': 'application/json'
# # # # # # # # # # # # # # # #     # }


# # # # # # # # # # # # # # # #     # 1. Combine the keys with a colon
# # # # # # # # # # # # # # # #     raw_token = "5BA4B542D3654105BCDB197D8FE4A23C:E4E4E336283D4A69891CA03BE85D4A57"
    
# # # # # # # # # # # # # # # #     # 2. Base64 encode the combined string
# # # # # # # # # # # # # # # #     token_bytes = raw_token.encode('utf-8')
# # # # # # # # # # # # # # # #     encoded_token = base64.b64encode(token_bytes).decode('utf-8')
    
# # # # # # # # # # # # # # # #     # 3. Send it WITHOUT the <token> tags
# # # # # # # # # # # # # # # #     headers = {
# # # # # # # # # # # # # # # #         'Authorization': f'AfasToken {encoded_token}',
# # # # # # # # # # # # # # # #         'Content-Type': 'application/json'
# # # # # # # # # # # # # # # #     }
# # # # # # # # # # # # # # # #     try:
# # # # # # # # # # # # # # # #         # 1. Calculate Date Range (Last Monday to Last Sunday)
# # # # # # # # # # # # # # # #         today = datetime.now()
# # # # # # # # # # # # # # # #         last_mon = (today - timedelta(days=today.weekday() + 7)).strftime('%Y-%m-%d')
# # # # # # # # # # # # # # # #         last_sun = (today - timedelta(days=today.weekday() + 1)).strftime('%Y-%m-%d')

# # # # # # # # # # # # # # # #         print(f"🚀 Starting sync for User ID: {user_id}")
# # # # # # # # # # # # # # # #         print(f"📅 Last week was: {last_mon} to {last_sun}")

# # # # # # # # # # # # # # # #         # 2. Fetch last week's entries
# # # # # # # # # # # # # # # #         get_url = (
# # # # # # # # # # # # # # # #             f"{AFAS_BASE_URL}/connectors/Profit_Realization"
# # # # # # # # # # # # # # # #             f"?filterfieldids=EmployeeId,DateTime"
# # # # # # # # # # # # # # # #             f"&filtervalues={user_id},{last_mon};{last_sun}"
# # # # # # # # # # # # # # # #             f"&operatortypes=1,9"
# # # # # # # # # # # # # # # #         )
        
# # # # # # # # # # # # # # # #         print(f"🔗 Requesting data from AFAS...")
# # # # # # # # # # # # # # # #         response = requests.get(get_url, headers=headers)

# # # # # # # # # # # # # # # #         if response.status_code != 200:
# # # # # # # # # # # # # # # #             print(f"❌ AFAS Connection Failed ({response.status_code})")
# # # # # # # # # # # # # # # #             print(f"Response Body: {response.text}")
# # # # # # # # # # # # # # # #             return

# # # # # # # # # # # # # # # #         source_data = response.json().get('rows', [])

# # # # # # # # # # # # # # # #         if not source_data:
# # # # # # # # # # # # # # # #             print(f"ℹ️ No hours found for {user_id} in the target range.")
# # # # # # # # # # # # # # # #             return

# # # # # # # # # # # # # # # #         print(f"✅ Found {len(source_data)} entries. Beginning copy...")

# # # # # # # # # # # # # # # #         # 3. Post entries to the current week
# # # # # # # # # # # # # # # #         success_count = 0
# # # # # # # # # # # # # # # #         for entry in source_data:
# # # # # # # # # # # # # # # #             original_date = datetime.strptime(entry['Da'], '%Y-%m-%d')
# # # # # # # # # # # # # # # #             new_date = (original_date + timedelta(days=7)).strftime('%Y-%m-%d')
            
# # # # # # # # # # # # # # # #             payload = {
# # # # # # # # # # # # # # # #                 "PtRealization": {
# # # # # # # # # # # # # # # #                     "Element": {
# # # # # # # # # # # # # # # #                         "Fields": {
# # # # # # # # # # # # # # # #                             "DaTi": new_date,
# # # # # # # # # # # # # # # #                             "EmId": user_id,
# # # # # # # # # # # # # # # #                             "PrId": entry.get('PrId', '82'),
# # # # # # # # # # # # # # # #                             "StTi": entry.get('StTi', '09:00:00'),
# # # # # # # # # # # # # # # #                             "EnTi": entry.get('EnTi', '17:00:00'),
# # # # # # # # # # # # # # # #                             "Ap": True,
# # # # # # # # # # # # # # # #                             "Pr": True
# # # # # # # # # # # # # # # #                         }
# # # # # # # # # # # # # # # #                     }
# # # # # # # # # # # # # # # #                 }
# # # # # # # # # # # # # # # #             }
            
# # # # # # # # # # # # # # # #             post_res = requests.post(
# # # # # # # # # # # # # # # #                 f"{AFAS_BASE_URL}/connectors/PtRealization", 
# # # # # # # # # # # # # # # #                 json=payload, 
# # # # # # # # # # # # # # # #                 headers=headers
# # # # # # # # # # # # # # # #             )
            
# # # # # # # # # # # # # # # #             if post_res.status_code in [200, 201, 204]:
# # # # # # # # # # # # # # # #                 print(f"✔️ Copied: {entry.get('PrId', 'Work')} on {new_date}")
# # # # # # # # # # # # # # # #                 success_count += 1
# # # # # # # # # # # # # # # #             else:
# # # # # # # # # # # # # # # #                 print(f"⚠️ Failed to copy entry for {new_date}: {post_res.text}")

# # # # # # # # # # # # # # # #         print(f"🎉 Done! Successfully synced {success_count} entries for {user_id}.")

# # # # # # # # # # # # # # # #     except Exception as e:
# # # # # # # # # # # # # # # #         print(f"❌ Script Error: {e}")

# # # # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # # # #     if len(sys.argv) > 2 and sys.argv[1] == '--user':
# # # # # # # # # # # # # # # #         target_user = sys.argv[2]
# # # # # # # # # # # # # # # #         sync_hours(target_user)
# # # # # # # # # # # # # # # #     else:
# # # # # # # # # # # # # # # #         print("❌ Error: No User ID provided. Usage: python copy_hours.py --user <ID>")


# # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # import sys
# # # # # # # # # # # # # # # # # import requests
# # # # # # # # # # # # # # # # # from datetime import datetime, timedelta

# # # # # # # # # # # # # # # # # # --- CONFIG ---
# # # # # # # # # # # # # # # # # # Pulling the token from GitHub Secrets for security
# # # # # # # # # # # # # # # # # AFAS_TOKEN = os.getenv("AFAS_TOKEN")
# # # # # # # # # # # # # # # # # AFAS_BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

# # # # # # # # # # # # # # # # # def sync_hours(user_id):
# # # # # # # # # # # # # # # # #     """Copies hours for a specific user from last week to the current week."""
    
# # # # # # # # # # # # # # # # #     # Validation: Ensure we actually have a token
# # # # # # # # # # # # # # # # #     if not AFAS_TOKEN:
# # # # # # # # # # # # # # # # #         print("❌ Error: AFAS_TOKEN environment variable is missing!")
# # # # # # # # # # # # # # # # #         return

# # # # # # # # # # # # # # # # #     headers = {
# # # # # # # # # # # # # # # # #         # 'Authorization': f'AfasToken {AFAS_TOKEN}',
# # # # # # # # # # # # # # # # #         'Authorization': f'AfasToken <token>{AFAS_TOKEN}</token>',
# # # # # # # # # # # # # # # # #         'Content-Type': 'application/json'
# # # # # # # # # # # # # # # # #     }

# # # # # # # # # # # # # # # # #     try:
# # # # # # # # # # # # # # # # #         # Calculate Dates
# # # # # # # # # # # # # # # # #         today = datetime.now()
# # # # # # # # # # # # # # # # #         # Last Monday
# # # # # # # # # # # # # # # # #         last_mon = (today - timedelta(days=today.weekday() + 7)).strftime('%Y-%m-%d')
# # # # # # # # # # # # # # # # #         # Last Sunday
# # # # # # # # # # # # # # # # #         last_sun = (today - timedelta(days=today.weekday() + 1)).strftime('%Y-%m-%d')

# # # # # # # # # # # # # # # # #         print(f"🚀 Starting sync for User ID: {user_id}")
# # # # # # # # # # # # # # # # #         print(f"📅 Looking for hours between {last_mon} and {last_sun}...")

# # # # # # # # # # # # # # # # #         # 1. FETCH DATA
# # # # # # # # # # # # # # # # #         get_url = f"{AFAS_BASE_URL}/connectors/Profit_Realization?filterfieldids=EmployeeId,DateTime&filtervalues={user_id},{last_mon};{last_sun}&operatortypes=1,9"

# # # # # # # # # # # # # # # # #         print(f"Token starts with: {AFAS_TOKEN[:5]}... and ends with: {AFAS_TOKEN[-5:]}")
# # # # # # # # # # # # # # # # #         response = requests.get(get_url, headers=headers)

# # # # # # # # # # # # # # # # #         # Check if the GET request worked
# # # # # # # # # # # # # # # # #         if response.status_code != 200:
# # # # # # # # # # # # # # # # #             print(f"❌ AFAS GET Error ({response.status_code}): {response.text}")
# # # # # # # # # # # # # # # # #             return

# # # # # # # # # # # # # # # # #         # Try to parse JSON safely
# # # # # # # # # # # # # # # # #         try:
# # # # # # # # # # # # # # # # #             source_data = response.json().get('rows', [])
# # # # # # # # # # # # # # # # #         except ValueError:
# # # # # # # # # # # # # # # # #             print("❌ Failed to decode JSON. AFAS sent back something else:")
# # # # # # # # # # # # # # # # #             print(response.text)
# # # # # # # # # # # # # # # # #             return

# # # # # # # # # # # # # # # # #         if not source_data:
# # # # # # # # # # # # # # # # #             print(f"ℹ️ No hours found for {user_id} in the previous week.")
# # # # # # # # # # # # # # # # #             return

# # # # # # # # # # # # # # # # #         print(f"✅ Found {len(source_data)} entries. Copying to current week...")

# # # # # # # # # # # # # # # # #         # 2. POST DATA (COPYING)
# # # # # # # # # # # # # # # # #         for entry in source_data:
# # # # # # # # # # # # # # # # #             # Shift the date forward by 7 days
# # # # # # # # # # # # # # # # #             original_date = datetime.strptime(entry['Da'], '%Y-%m-%d')
# # # # # # # # # # # # # # # # #             new_date = (original_date + timedelta(days=7)).strftime('%Y-%m-%d')
            
# # # # # # # # # # # # # # # # #             payload = {
# # # # # # # # # # # # # # # # #                 "PtRealization": {
# # # # # # # # # # # # # # # # #                     "Element": {
# # # # # # # # # # # # # # # # #                         "Fields": {
# # # # # # # # # # # # # # # # #                             "DaTi": new_date,
# # # # # # # # # # # # # # # # #                             "EmId": user_id,
# # # # # # # # # # # # # # # # #                             "PrId": entry.get('PrId', '82'),
# # # # # # # # # # # # # # # # #                             "StTi": entry.get('StTi', '09:00:00'),
# # # # # # # # # # # # # # # # #                             "EnTi": entry.get('EnTi', '17:00:00'),
# # # # # # # # # # # # # # # # #                             "Ap": True,
# # # # # # # # # # # # # # # # #                             "Pr": True
# # # # # # # # # # # # # # # # #                         }
# # # # # # # # # # # # # # # # #                     }
# # # # # # # # # # # # # # # # #                 }
# # # # # # # # # # # # # # # # #             }
            
# # # # # # # # # # # # # # # # #             post_res = requests.post(f"{AFAS_BASE_URL}/connectors/PtRealization", json=payload, headers=headers)
            
# # # # # # # # # # # # # # # # #             if post_res.status_code in [200, 201, 204]:
# # # # # # # # # # # # # # # # #                 print(f"✔️ Successfully copied entry for {new_date}")
# # # # # # # # # # # # # # # # #             else:
# # # # # # # # # # # # # # # # #                 print(f"⚠️ Failed to copy entry for {new_date}: {post_res.text}")

# # # # # # # # # # # # # # # # #         print(f"🎉 Process finished for {user_id}!")

# # # # # # # # # # # # # # # # #     except Exception as e:
# # # # # # # # # # # # # # # # #         print(f"❌ Unexpected Script Error: {e}")

# # # # # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # # # # #     # This part reads the '--user 90114' part from your GitHub Action
# # # # # # # # # # # # # # # # #     if len(sys.argv) > 2 and sys.argv[1] == '--user':
# # # # # # # # # # # # # # # # #         target_user = sys.argv[2]
# # # # # # # # # # # # # # # # #         sync_hours(target_user)
# # # # # # # # # # # # # # # # #     else:
# # # # # # # # # # # # # # # # #         print("❌ Error: No User ID provided in command line arguments.")


# # # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # # import sys
# # # # # # # # # # # # # # # # # # import requests
# # # # # # # # # # # # # # # # # # from datetime import datetime, timedelta

# # # # # # # # # # # # # # # # # # # Config from your original script
# # # # # # # # # # # # # # # # # # AFAS_TOKEN = os.getenv("AFAS_TOKEN", '5BA4B542D3654105BCDB197D8FE4A23C') # Safely pulled from GitHub Secrets
# # # # # # # # # # # # # # # # # # AFAS_BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

# # # # # # # # # # # # # # # # # # def sync_hours(user_id):
# # # # # # # # # # # # # # # # # #     headers = {'Authorization': f'AfasToken {AFAS_TOKEN}', 'Content-Type': 'application/json'}
# # # # # # # # # # # # # # # # # #     try:
# # # # # # # # # # # # # # # # # #         print(f"Starting sync for {user_id}...")
# # # # # # # # # # # # # # # # # #         today = datetime.now()
# # # # # # # # # # # # # # # # # #         last_mon = (today - timedelta(days=today.weekday() + 7)).strftime('%Y-%m-%d')
# # # # # # # # # # # # # # # # # #         last_sun = (today - timedelta(days=today.weekday() + 1)).strftime('%Y-%m-%d')

# # # # # # # # # # # # # # # # # #         # 1. Fetch last week's data
# # # # # # # # # # # # # # # # # #         get_url = f"{AFAS_BASE_URL}/connectors/Profit_Realization?filterfieldids=EmployeeId,DateTime&filtervalues={user_id},{last_mon};{last_sun}&operatortypes=1,9"
# # # # # # # # # # # # # # # # # #         source_data = requests.get(get_url, headers=headers).json().get('rows', [])

# # # # # # # # # # # # # # # # # #         if not source_data:
# # # # # # # # # # # # # # # # # #             print(f"No hours found for {user_id} between {last_mon} and {last_sun}.")
# # # # # # # # # # # # # # # # # #             return

# # # # # # # # # # # # # # # # # #         # 2. Copy to this week
# # # # # # # # # # # # # # # # # #         for entry in source_data:
# # # # # # # # # # # # # # # # # #             new_date = (datetime.strptime(entry['Da'], '%Y-%m-%d') + timedelta(days=7)).strftime('%Y-%m-%d')
# # # # # # # # # # # # # # # # # #             payload = {
# # # # # # # # # # # # # # # # # #                 "PtRealization": {
# # # # # # # # # # # # # # # # # #                     "Element": {
# # # # # # # # # # # # # # # # # #                         "Fields": {
# # # # # # # # # # # # # # # # # #                             "DaTi": new_date, 
# # # # # # # # # # # # # # # # # #                             "EmId": user_id, 
# # # # # # # # # # # # # # # # # #                             "PrId": entry.get('PrId', '82'), 
# # # # # # # # # # # # # # # # # #                             "StTi": entry.get('StTi', '09:00:00'), 
# # # # # # # # # # # # # # # # # #                             "EnTi": entry.get('EnTi', '17:00:00'), 
# # # # # # # # # # # # # # # # # #                             "Ap": True, 
# # # # # # # # # # # # # # # # # #                             "Pr": True
# # # # # # # # # # # # # # # # # #                         }
# # # # # # # # # # # # # # # # # #                     }
# # # # # # # # # # # # # # # # # #                 }
# # # # # # # # # # # # # # # # # #             }
# # # # # # # # # # # # # # # # # #             res = requests.post(f"{AFAS_BASE_URL}/connectors/PtRealization", json=payload, headers=headers)
# # # # # # # # # # # # # # # # # #             print(f"Sent entry for {new_date}: Status {res.status_code}")

# # # # # # # # # # # # # # # # # #         print(f"✅ [{user_id}] Sync complete.")

# # # # # # # # # # # # # # # # # #     except Exception as e:
# # # # # # # # # # # # # # # # # #         print(f"❌ [{user_id}] Sync error: {e}")

# # # # # # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # # # # # #     # Get user_id from GitHub Action payload
# # # # # # # # # # # # # # # # # #     if len(sys.argv) > 2 and sys.argv[1] == '--user':
# # # # # # # # # # # # # # # # # #         target_user = sys.argv[2]
# # # # # # # # # # # # # # # # # #         sync_hours(target_user)
# # # # # # # # # # # # # # # # # #     else:
# # # # # # # # # # # # # # # # # #         print("No user provided to script.")
