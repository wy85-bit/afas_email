from http.server import BaseHTTPRequestHandler
import base64, requests, json
from urllib.parse import urlparse, parse_qs

# --- CONFIGURATION ---
AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices/connectors"

def get_headers():
    """Encodes the working token for environment 90114."""
    token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
    return {'Authorization': f'AfasToken {token}', 'Content-Type': 'application/json'}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Get the Employee ID from the button click
        query = parse_qs(urlparse(self.path).query)
        user_id = query.get('user_id', [None])[0]

        if not user_id or user_id == "Unknown":
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Error: No valid Employee ID found.")
            return

        try:
            headers = get_headers()
            
            # 2. Fetch the specific hour rows for this user
            # We filter by EmployeeId so we only copy the right person's hours
            get_url = f"{BASE_URL}/Profit_Realization?filterfieldids=EmployeeId&filtervalues={user_id}"
            afas_resp = requests.get(get_url, headers=headers)
            data = afas_resp.json()
            rows = data.get('rows', [])

            # 3. Process each row and POST it back to AFAS
            success_count = 0
            for row in rows:
                # We map the data we found in your previous test
                # to the fields AFAS needs for a new entry.
                payload = {
                    "PtRealization": {
                        "Element": {
                            "Fields": {
                                "EmId": row.get('EmployeeId'),   # Employee ID
                                "PrId": row.get('ProjectID'),    # Project ID
                                "ItId": row.get('ItemCodeId'),   # Item Code
                                "Un": row.get('QuantityUnit'),   # Number of units
                                "Da": row.get('DateTime')        # The date
                            }
                        }
                    }
                }
                
                # Push the data to the UpdateConnector
                post_url = f"{BASE_URL}/PtRealization"
                post_resp = requests.post(post_url, headers=headers, json=payload)
                
                if post_resp.status_code in [200, 201]:
                    success_count += 1

            # 4. Show the clean Success Page
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8') # Fixes the âœ... encoding
            self.end_headers()
            
            html = f"""
            <html><body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                <h1 style="color: #0070f3;">✅ Mission Accomplished!</h1>
                <p style="font-size: 1.2em;">Successfully copied <b>{success_count}</b> hour entries for Employee <b>{user_id}</b>.</p>
                <p style="color: #666;">The AFAS environment 90114 has been updated.</p>
            </body></html>
            """
            self.wfile.write(html.encode('utf-8'))

        except Exception as e:
            # If something fails, we show the exact error (like the one in image_bdad40.png)
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
# from http.server import BaseHTTPRequestHandler
# import json
# from urllib.parse import urlparse, parse_qs

# class handler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         query = parse_qs(urlparse(self.path).query)
#         user_id = query.get('user_id', ['Unknown'])[0]

#         self.send_response(200)
#         # Added charset=utf-8 to fix the funny characters!
#         self.send_header('Content-type', 'text/html; charset=utf-8') 
#         self.end_headers()
        
#         success_page = f"""
#         <html>
#             <head><meta charset="UTF-8"></head>
#             <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
#                 <h1 style="color: #0070f3;">✅ Success!</h1>
#                 <p style="font-size: 1.2em;">Hours for Employee <b>{user_id}</b> have been processed in AFAS 90114.</p>
#                 <p style="color: #666;">You can safely close this window now.</p>
#             </body>
#         </html>
#         """
#         self.wfile.write(success_page.encode('utf-8'))

# # from http.server import BaseHTTPRequestHandler
# # import json
# # from urllib.parse import urlparse, parse_qs

# # class handler(BaseHTTPRequestHandler):
# #     def do_GET(self):
# #         # 1. Parse the User ID from the URL
# #         query = parse_qs(urlparse(self.path).query)
# #         user_id = query.get('user_id', ['Unknown'])[0]

# #         self.send_response(200)
# #         self.send_header('Content-type', 'text/html')
# #         self.end_headers()
        
# #         # 2. Show a nice success message
# #         success_page = f"""
# #         <html><body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
# #             <h1 style="color: #0070f3;">✅ Success!</h1>
# #             <p>Hours for Employee <b>{user_id}</b> have been processed in AFAS 90114.</p>
# #             <p>You can close this window now.</p>
# #         </body></html>
# #         """
# #         self.wfile.write(success_page.encode())


# # # from http.server import BaseHTTPRequestHandler
# # # from urllib.parse import urlparse, parse_qs
# # # import json
# # # # Import your logic from the file we named earlier
# # # from post_hours_for_employee import post_hours, get_auth_header 

# # # class handler(BaseHTTPRequestHandler):
# # #     def do_GET(self):
# # #         # 1. Parse the user_id from the URL link
# # #         query_components = parse_qs(urlparse(self.path).query)
# # #         user_id = query_components.get("user_id", [None])[0]

# # #         if not user_id:
# # #             self.send_response(400)
# # #             self.end_headers()
# # #             self.wfile.write(b"Error: No User ID provided.")
# # #             return

# # #         # 2. Logic: In a real app, you'd fetch the saved hours from a DB here.
# # #         # For this example, let's assume we have the hours ready to go.
# # #         # This calls your AFAS UpdateConnector logic
# # #         dummy_hours = [{"Project": "1001", "Aantal": 8.0, "Toelichting": "Copied via Email"}]
# # #         result = post_hours(user_id, dummy_hours)

# # #         # 3. Respond to the employee in the browser
# # #         self.send_response(200)
# # #         self.send_header('Content-type', 'text/html')
# # #         self.end_headers()
        
# # #         response_html = f"""
# # #         <html>
# # #             <body style="font-family: sans-serif; text-align: center; padding: 50px;">
# # #                 <h1>✅ Success!</h1>
# # #                 <p>Hi {user_id}, your hours have been copied to AFAS environment 90114.</p>
# # #                 <p>Processed {result['success']} entries.</p>
# # #             </body>
# # #         </html>
# # #         """
# # #         self.wfile.write(response_html.encode())
