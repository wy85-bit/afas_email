from http.server import BaseHTTPRequestHandler
import base64, requests, json
from urllib.parse import urlparse, parse_qs

# --- CONFIGURATION ---
AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices/connectors"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        user_id = query.get('user_id', [None])[0]
        
        # 1. Prepare Headers
        token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
        headers = {'Authorization': f'AfasToken {token}', 'Content-Type': 'application/json'}

        try:
            # 2. Fetch ALL rows (more reliable than URL filtering)
            afas_resp = requests.get(f"{BASE_URL}/Profit_Realization", headers=headers)
            all_data = afas_resp.json()
            all_rows = all_data.get('rows', [])

            # 3. Filter for the specific employee in Python
            my_rows = [r for r in all_rows if str(r.get('EmployeeId')) == str(user_id)]
            
            success_count = 0
            errors = []

            # 4. Map and Push to AFAS UpdateConnector
            for row in my_rows:
                # AFAS UpdateConnectors use specific short codes (EmId, PrId, etc.)
                payload = {
                    "PtRealization": {
                        "Element": {
                            "Fields": {
                                "EmId": row.get('EmployeeId'),   #
                                "PrId": row.get('ProjectID'),    #
                                "ItId": row.get('ItemCodeId'),   #
                                "UnId": row.get('UnitId'),       #
                                "Qu": row.get('QuantityUnit'),   #
                                "Da": row.get('DateTime')        #
                            }
                        }
                    }
                }
                
                post_resp = requests.post(f"{BASE_URL}/PtRealization", headers=headers, json=payload)
                if post_resp.status_code in [200, 201]:
                    success_count += 1
                else:
                    errors.append(post_resp.text)

            # 5. Show the Final Success Page
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            status_color = "#0070f3" if success_count > 0 else "#e00"
            html = f"""
            <html><body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                <h1 style="color: {status_color};">{'✅ Success!' if success_count > 0 else '⚠️ Note'}</h1>
                <p style="font-size: 1.2em;">Processed <b>{success_count}</b> entries for Employee <b>{user_id}</b>.</p>
                <p>Found {len(my_rows)} total records for this ID in AFAS 90114.</p>
                {"<p style='color:red'>Errors: " + str(errors) + "</p>" if errors else ""}
            </body></html>
            """
            self.wfile.write(html.encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error logic: {str(e)}".encode())


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
