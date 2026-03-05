from http.server import BaseHTTPRequestHandler
import base64, requests, json, datetime
from urllib.parse import urlparse, parse_qs

# --- CONFIGURATION ---
AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices/connectors"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        user_id = query.get('user_id', ['1000077'])[0] 
        
        token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
        headers = {'Authorization': f'AfasToken {token}', 'Content-Type': 'application/json'}

        try:
            # 1. FETCH RAW DATA (No filters, just get everything)
            afas_resp = requests.get(f"{BASE_URL}/Profit_Realization", headers=headers)
            all_rows = afas_resp.json().get('rows', [])
            my_rows = [r for r in all_rows if str(r.get('EmployeeId')) == str(user_id)]
            
            success_count = 0
            error_msg = ""
            # We will try to backdate to February to dodge the March 'Period' error
            safe_date = "2026-02-25" 

            # 2. ATTEMPT PUSH
            for row in my_rows:
                payload = {"PtRealization": {"Element": {"Fields": {
                    "EmId": row.get('EmployeeId'), "PrId": row.get('ProjectID'),
                    "ItId": row.get('ItemCodeId'), "UnId": row.get('UnitId'),
                    "Qu": row.get('QuantityUnit'), "Da": safe_date 
                }}}}
                post_resp = requests.post(f"{BASE_URL}/PtRealization", headers=headers, json=payload)
                if post_resp.status_code in [200, 201]:
                    success_count += 1
                else:
                    error_msg = post_resp.json().get('externalMessage', 'Unknown Error')

            # 3. VERBOSE RESPONSE (So we can see exactly what's happening)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            status_color = "#28a745" if success_count > 0 else "#dc3545"
            html = f"""
            <html><body style="font-family: sans-serif; text-align: center; padding: 50px; background: #f4f7f6;">
                <div style="background: white; display: inline-block; padding: 40px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-top: 10px solid {status_color};">
                    <h1 style="color: {status_color};">Status: {success_count} Approved</h1>
                    <p>Testing with User: <b>{user_id}</b></p>
                    <p>Found <b>{len(my_rows)}</b> open entries in AFAS.</p>
            """
            
            if error_msg:
                html += f'<p style="color: red; background: #ffeeee; padding: 10px; border-radius: 5px;"><b>Latest AFAS Error:</b> {error_msg}</p>'
            
            if len(my_rows) > 0:
                html += "<h3>Entries we tried to approve:</h3><table border='1' style='margin:auto; border-collapse: collapse; font-size: 0.8em;'>"
                html += "<tr><th>Project</th><th>Units</th><th>Orig. Date</th></tr>"
                for r in my_rows[:5]: # Show first 5
                    html += f"<tr><td>{r.get('ProjectID')}</td><td>{r.get('QuantityUnit')}</td><td>{r.get('Date')}</td></tr>"
                html += "</table>"

            html += f"""
                    <p style="margin-top: 20px;"><a href="?user_id=1000077" style="color: #007bff;">Retry 1000077</a> | <a href="?user_id=90114" style="color: #007bff;">Retry 90114</a></p>
                </div>
            </body></html>
            """
            self.wfile.write(html.encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())


# from http.server import BaseHTTPRequestHandler
# import base64, requests, json, datetime
# from urllib.parse import urlparse, parse_qs

# # --- CONFIGURATION ---
# AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
# BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices/connectors"

# class handler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         query = parse_qs(urlparse(self.path).query)
#         user_id = query.get('user_id', [None])[0]
        
#         token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
#         headers = {'Authorization': f'AfasToken {token}', 'Content-Type': 'application/json'}

#         try:
#             # --- NEW: VALIDATION STEP ---
#             # Check if this employee exists and is active
#             emp_resp = requests.get(f"{BASE_URL}/Profit_Employee?filterfieldids=EmployeeId&filtervalues={user_id}&operatortypes=1", headers=headers)
#             emp_data = emp_resp.json().get('rows', [])
            
#             is_active = False
#             suggested_id = None

#             if emp_data:
#                 # If they have an 'EndDate' (or similar), they might be out of service
#                 # Adjust 'EmploymentEnd' based on your actual AFAS Connector field name
#                 end_date = emp_data[0].get('EmploymentEnd')
#                 if not end_date or datetime.datetime.strptime(end_date, "%Y-%m-%d") > datetime.datetime.now():
#                     is_active = True
            
#             # If not active, find a "live" one to suggest (Top 1 active)
#             if not is_active:
#                 suggest_resp = requests.get(f"{BASE_URL}/Profit_Employee?take=1", headers=headers)
#                 suggestions = suggest_resp.json().get('rows', [])
#                 if suggestions:
#                     suggested_id = suggestions[0].get('EmployeeId')

#             # --- ORIGINAL LOGIC (Only if active) ---
#             success_count = 0
#             error_details = []
#             today = datetime.datetime.now().strftime("%Y-%m-%d")

#             if is_active:
#                 afas_resp = requests.get(f"{BASE_URL}/Profit_Realization", headers=headers)
#                 all_rows = afas_resp.json().get('rows', [])
#                 my_rows = [r for r in all_rows if str(r.get('EmployeeId')) == str(user_id)]
                
#                 for row in my_rows:
#                     payload = {
#                         "PtRealization": {
#                             "Element": {
#                                 "Fields": {
#                                     "EmId": row.get('EmployeeId'),
#                                     "PrId": row.get('ProjectID'),
#                                     "ItId": row.get('ItemCodeId'),
#                                     "UnId": row.get('UnitId'),
#                                     "Qu": row.get('QuantityUnit'),
#                                     "Da": today 
#                                 }
#                             }
#                         }
#                     }
#                     post_resp = requests.post(f"{BASE_URL}/PtRealization", headers=headers, json=payload)
#                     if post_resp.status_code in [200, 201]:
#                         success_count += 1
#                     else:
#                         error_details.append(post_resp.json().get('externalMessage', 'Unknown Error'))

#             # --- DYNAMIC HTML RESPONSE ---
#             self.send_response(200)
#             self.send_header('Content-type', 'text/html; charset=utf-8')
#             self.end_headers()
            
#             status_color = "#0070f3" if is_active else "#ff4d4d"
#             status_msg = "✅ Active Employee Found" if is_active else "⚠️ Employee Out of Service"
            
#             html = f"""
#             <html><body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
#                 <h1 style="color: {status_color};">{status_msg}</h1>
#                 <p>Checking ID: <b>{user_id}</b></p>
#             """
            
#             if not is_active and suggested_id:
#                 html += f"""
#                 <div style="background: #fff5f5; border: 1px solid #ff4d4d; display: inline-block; padding: 20px; border-radius: 8px;">
#                     <p>Employee <b>{user_id}</b> is no longer with us.</p>
#                     <p>Try testing with an active ID like: <a href="?user_id={suggested_id}"><b>{suggested_id}</b></a></p>
#                 </div>
#                 """
#             elif is_active:
#                 html += f"<p>Processed <b>{success_count}</b> entries.</p>"
#                 if error_details:
#                     html += f'<p style="color:red"><b>AFAS Error:</b> {error_details[0]}</p>'

#             html += "</body></html>"
#             self.wfile.write(html.encode('utf-8'))

#         except Exception as e:
#             self.send_response(500)
#             self.end_headers()
#             self.wfile.write(str(e).encode())

# # from http.server import BaseHTTPRequestHandler
# # import base64, requests, json, datetime
# # from urllib.parse import urlparse, parse_qs

# # # --- CONFIGURATION ---
# # AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
# # BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices/connectors"

# # class handler(BaseHTTPRequestHandler):
# #     def do_GET(self):
# #         query = parse_qs(urlparse(self.path).query)
# #         user_id = query.get('user_id', [None])[0]
        
# #         token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
# #         headers = {'Authorization': f'AfasToken {token}', 'Content-Type': 'application/json'}

# #         try:
# #             # 1. Fetch the rows
# #             afas_resp = requests.get(f"{BASE_URL}/Profit_Realization", headers=headers)
# #             all_rows = afas_resp.json().get('rows', [])
# #             my_rows = [r for r in all_rows if str(r.get('EmployeeId')) == str(user_id)]
            
# #             # 2. Get Today's Date in AFAS format (YYYY-MM-DD)
# #             today = datetime.datetime.now().strftime("%Y-%m-%d")
            
# #             success_count = 0
# #             error_details = []

# #             # 3. Push to AFAS with the Date Fix
# #             for row in my_rows:
# #                 payload = {
# #                     "PtRealization": {
# #                         "Element": {
# #                             "Fields": {
# #                                 "EmId": row.get('EmployeeId'),
# #                                 "PrId": row.get('ProjectID'),
# #                                 "ItId": row.get('ItemCodeId'),
# #                                 "UnId": row.get('UnitId'),
# #                                 "Qu": row.get('QuantityUnit'),
# #                                 "Da": today  # FIX: Using today's date instead of 2020!
# #                             }
# #                         }
# #                     }
# #                 }
                
# #                 post_resp = requests.post(f"{BASE_URL}/PtRealization", headers=headers, json=payload)
# #                 if post_resp.status_code in [200, 201]:
# #                     success_count += 1
# #                 else:
# #                     error_details.append(post_resp.json().get('externalMessage', 'Unknown Error'))

# #             # 4. Final Success Page
# #             self.send_response(200)
# #             self.send_header('Content-type', 'text/html; charset=utf-8')
# #             self.end_headers()
            
# #             html = f"""
# #             <html><body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
# #                 <h1 style="color: #0070f3;">{'✅ Success!' if success_count > 0 else '❌ Action Needed'}</h1>
# #                 <p style="font-size: 1.2em;">Processed <b>{success_count}</b> entries for Employee <b>{user_id}</b>.</p>
# #                 {f'<p style="color:red"><b>AFAS says:</b> {error_details[0]}</p>' if error_details else ''}
# #                 <p style="color: #666;">Entries were sent with date: {today}</p>
# #             </body></html>
# #             """
# #             self.wfile.write(html.encode('utf-8'))

# #         except Exception as e:
# #             self.send_response(500)
# #             self.end_headers()
# #             self.wfile.write(str(e).encode())


# # # from http.server import BaseHTTPRequestHandler
# # # import json
# # # from urllib.parse import urlparse, parse_qs

# # # class handler(BaseHTTPRequestHandler):
# # #     def do_GET(self):
# # #         query = parse_qs(urlparse(self.path).query)
# # #         user_id = query.get('user_id', ['Unknown'])[0]

# # #         self.send_response(200)
# # #         # Added charset=utf-8 to fix the funny characters!
# # #         self.send_header('Content-type', 'text/html; charset=utf-8') 
# # #         self.end_headers()
        
# # #         success_page = f"""
# # #         <html>
# # #             <head><meta charset="UTF-8"></head>
# # #             <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
# # #                 <h1 style="color: #0070f3;">✅ Success!</h1>
# # #                 <p style="font-size: 1.2em;">Hours for Employee <b>{user_id}</b> have been processed in AFAS 90114.</p>
# # #                 <p style="color: #666;">You can safely close this window now.</p>
# # #             </body>
# # #         </html>
# # #         """
# # #         self.wfile.write(success_page.encode('utf-8'))

# # # # from http.server import BaseHTTPRequestHandler
# # # # import json
# # # # from urllib.parse import urlparse, parse_qs

# # # # class handler(BaseHTTPRequestHandler):
# # # #     def do_GET(self):
# # # #         # 1. Parse the User ID from the URL
# # # #         query = parse_qs(urlparse(self.path).query)
# # # #         user_id = query.get('user_id', ['Unknown'])[0]

# # # #         self.send_response(200)
# # # #         self.send_header('Content-type', 'text/html')
# # # #         self.end_headers()
        
# # # #         # 2. Show a nice success message
# # # #         success_page = f"""
# # # #         <html><body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
# # # #             <h1 style="color: #0070f3;">✅ Success!</h1>
# # # #             <p>Hours for Employee <b>{user_id}</b> have been processed in AFAS 90114.</p>
# # # #             <p>You can close this window now.</p>
# # # #         </body></html>
# # # #         """
# # # #         self.wfile.write(success_page.encode())


# # # # # from http.server import BaseHTTPRequestHandler
# # # # # from urllib.parse import urlparse, parse_qs
# # # # # import json
# # # # # # Import your logic from the file we named earlier
# # # # # from post_hours_for_employee import post_hours, get_auth_header 

# # # # # class handler(BaseHTTPRequestHandler):
# # # # #     def do_GET(self):
# # # # #         # 1. Parse the user_id from the URL link
# # # # #         query_components = parse_qs(urlparse(self.path).query)
# # # # #         user_id = query_components.get("user_id", [None])[0]

# # # # #         if not user_id:
# # # # #             self.send_response(400)
# # # # #             self.end_headers()
# # # # #             self.wfile.write(b"Error: No User ID provided.")
# # # # #             return

# # # # #         # 2. Logic: In a real app, you'd fetch the saved hours from a DB here.
# # # # #         # For this example, let's assume we have the hours ready to go.
# # # # #         # This calls your AFAS UpdateConnector logic
# # # # #         dummy_hours = [{"Project": "1001", "Aantal": 8.0, "Toelichting": "Copied via Email"}]
# # # # #         result = post_hours(user_id, dummy_hours)

# # # # #         # 3. Respond to the employee in the browser
# # # # #         self.send_response(200)
# # # # #         self.send_header('Content-type', 'text/html')
# # # # #         self.end_headers()
        
# # # # #         response_html = f"""
# # # # #         <html>
# # # # #             <body style="font-family: sans-serif; text-align: center; padding: 50px;">
# # # # #                 <h1>✅ Success!</h1>
# # # # #                 <p>Hi {user_id}, your hours have been copied to AFAS environment 90114.</p>
# # # # #                 <p>Processed {result['success']} entries.</p>
# # # # #             </body>
# # # # #         </html>
# # # # #         """
# # # # #         self.wfile.write(response_html.encode())
