from http.server import BaseHTTPRequestHandler
import base64, requests, json

# --- CONFIGURATION ---
AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices/connectors"
GET_CONNECTOR = "winnie"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
        headers = {'Authorization': f'AfasToken {token}', 'Content-Type': 'application/json'}

        try:
            test_date = "2025-01-06" # The first Monday of 2025
            final_iso_date = f"{test_date}T00:00:00"

            payload = {
                "PtRealizationWeek": {
                    "Element": {
                        "Fields": {
                            "EmId": "1000994",      
                            "PcOc": 105,
                            "ItCd": "1",
                            "UnTy": "Z",  # Adding Unit Type 'Z' as seen in your manual successful line
                            "Qu": 1.0,    
                            "Da": "2025-01-06T00:00:00" 
                        }
                    }
                }
            }
            
            # 2. TRY THE ALTERNATE CONNECTOR (To see if it exists)
            check_conn = requests.get(f"{BASE_URL}/KnPeriod?take=1", headers=headers)
            
            post_resp = requests.post(f"{BASE_URL}/PtRealizationWeek", headers=headers, json=payload)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html = f"""
            <html><body>
                <h1>AFAS Status: {post_resp.status_code}</h1>
                <p><b>Tried Date:</b> {test_date}</p>
                <pre>{post_resp.text}</pre>
                <hr>
                <p><b>KnPeriod Connector Check:</b> {check_conn.status_code} (200 = Found!)</p>
            </body></html>
            """
            self.wfile.write(html.encode('utf-8'))

        except Exception as e:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())

# from http.server import BaseHTTPRequestHandler
# import base64, requests, json

# # --- CONFIGURATION ---
# AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
# BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices/connectors"
# GET_CONNECTOR = "winnie" 

# class handler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
#         headers = {'Authorization': f'AfasToken {token}', 'Content-Type': 'application/json'}

#         try:
#             # 1. FETCH - Looking for the latest existing entry
#             afas_resp = requests.get(f"{BASE_URL}/{GET_CONNECTOR}?skip=0&take=1", headers=headers)
#             all_rows = afas_resp.json().get('rows', [])
            
#             if all_rows:
#                 # IMPORTANT: If AFAS returns a date with T00:00:00, we split it to keep it clean
#                 raw_date = all_rows[0].get('Datum', "2025-12-29")
#                 safe_date = raw_date.split('T')[0] 
#                 project = all_rows[0].get('Project', "VV")
#                 item = all_rows[0].get('Itemcode', "VZ")
#             else:
#                 safe_date = "2025-12-29" 
#                 project = "VV"
#                 item = "VZ"

#             # 2. CLONE - The "Safe" date for the payload
#             # We explicitly use safe_date (YYYY-MM-DD) + T00:00:00
#             final_iso_date = f"{safe_date}T00:00:00"

#             payload = {"PtRealization": {"Element": {"Fields": {
#                 "EmId": "1000994",      
#                 "PrId": project,        
#                 "ItId": item,           
#                 "Qu": 8.0,
#                 "Da": final_iso_date 
#             }}}}
            
#             post_resp = requests.post(f"{BASE_URL}/PtRealization", headers=headers, json=payload)
            
#             # 3. SHOW RESULT
#             self.send_response(200)
#             self.send_header('Content-type', 'text/html; charset=utf-8')
#             self.end_headers()
            
#             if post_resp.status_code in [200, 201]:
#                 html = f"""
#                 <html><body style="text-align:center; font-family:sans-serif; padding-top:100px; background-color:#f0fdf4;">
#                     <h1 style="color:#166534; font-size:60px;">✅ SUCCESS!</h1>
#                     <p style="font-size:24px;">The Banana is yours! Cloned to {final_iso_date}.</p>
#                 </body></html>
#                 """
#             else:
#                 html = f"""
#                 <html><body style="text-align:center; font-family:sans-serif; padding-top:100px; background-color:#fef2f2;">
#                     <h1 style="color:#991b1b; font-size:60px;">❌ FAILED</h1>
#                     <p>AFAS says: {post_resp.text}</p>
#                     <p>Sent Date: {final_iso_date}</p>
#                 </body></html>
#                 """
#             self.wfile.write(html.encode('utf-8'))

#         except Exception as e:
#             self.send_response(200)
#             self.end_headers()
#             self.wfile.write(f"Error: {str(e)}".encode())

# # from http.server import BaseHTTPRequestHandler
# # import base64, requests, json

# # # --- CONFIGURATION ---
# # AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
# # BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices/connectors"
# # GET_CONNECTOR = "winnie" 

# # class handler(BaseHTTPRequestHandler):
# #     def do_GET(self):
# #         token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
# #         headers = {'Authorization': f'AfasToken {token}', 'Content-Type': 'application/json'}

# #         try:
# #             # 1. FETCH - Looking for the latest existing entry
# #             afas_resp = requests.get(f"{BASE_URL}/{GET_CONNECTOR}?skip=0&take=1", headers=headers)
# #             all_rows = afas_resp.json().get('rows', [])
            
# #             if all_rows:
# #                 safe_date = all_rows[0].get('Datum')
# #                 project = all_rows[0].get('Project')
# #                 item = all_rows[0].get('Itemcode')
# #             else:
# #                 # Fallback to the first day of the 2026 period in the Week Projecten table
# #                 safe_date = "2025-12-29" 
# #                 project = "VV"
# #                 item = "VZ"

# #             # 2. CLONE - Using the explicit ISO timestamp
# #             # This 'T00:00:00' is often the secret to making the Projects module recognize the period
# #             # 2. CLONE - Cleaned up date format
# #             payload = {"PtRealization": {"Element": {"Fields": {
# #                 "EmId": "1000364",      
# #                 "PrId": project,        
# #                 "ItId": item,           
# #                 "Qu": 8.0,
# #                 # Make sure there is NO extra 'Z' or 'T00:00:00' at the end
# #                 "Da": "2025-01-16T00:00:00" 
# #             }}}}
                        
# #             post_resp = requests.post(f"{BASE_URL}/PtRealization", headers=headers, json=payload)
            
# #             # 3. SHOW RESULT
# #             self.send_response(200)
# #             self.send_header('Content-type', 'text/html; charset=utf-8')
# #             self.end_headers()
            
# #             if post_resp.status_code in [200, 201]:
# #                 html = f"""
# #                 <html><body style="text-align:center; font-family:sans-serif; padding-top:100px; background-color:#f0fdf4;">
# #                     <h1 style="color:#166534; font-size:60px;">✅ SUCCESS!</h1>
# #                     <p style="font-size:24px;">The Banana is yours! Cloned to {safe_date}.</p>
# #                 </body></html>
# #                 """
# #             else:
# #                 html = f"""
# #                 <html><body style="text-align:center; font-family:sans-serif; padding-top:100px; background-color:#fef2f2;">
# #                     <h1 style="color:#991b1b; font-size:60px;">❌ FAILED</h1>
# #                     <p>AFAS says: {post_resp.text}</p>
# #                     <p>Sent Date: {safe_date}T00:00:00</p>
# #                 </body></html>
# #                 """
# #             self.wfile.write(html.encode('utf-8'))

# #         except Exception as e:
# #             self.send_response(200)
# #             self.end_headers()
# #             self.wfile.write(f"Error: {str(e)}".encode())


# # # from http.server import BaseHTTPRequestHandler
# # # import base64, requests, json

# # # # --- CONFIGURATION ---
# # # AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
# # # BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices/connectors"
# # # GET_CONNECTOR = "winnie" 

# # # class handler(BaseHTTPRequestHandler):
# # #     def do_GET(self):
# # #         token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
# # #         headers = {'Authorization': f'AfasToken {token}', 'Content-Type': 'application/json'}

# # #         try:
# # #             # 1. FETCH - Find the most recent date AFAS has on file for you
# # #             afas_resp = requests.get(f"{BASE_URL}/{GET_CONNECTOR}?skip=0&take=1", headers=headers)
# # #             all_rows = afas_resp.json().get('rows', [])
            
# # #             # 2. MATCH - If we find a row, we use THAT date (the Safe Zone)
# # #             # 2. MATCH - If we find a row, we use THAT date (the Safe Zone)
# # #             if all_rows:
# # #                 safe_date = all_rows[0].get('Datum')
# # #                 project = all_rows[0].get('Project')
# # #                 item = all_rows[0].get('Itemcode')
# # #             else:
# # #                 # Testing the "Time Machine" theory: 
# # #                 # Checking if the module is stuck in 2024.
# # #                 safe_date = "2024-01-15" 
# # #                 project = "VV"
# # #                 item = "VZ"

# # #             # 3. CLONE - Using your real ID 1000994 and the Safe Date
# # #            # 3. CLONE - Using your real ID and a formatted date
# # #             payload = {"PtRealization": {"Element": {"Fields": {
# # #                 "EmId": "1000364",
# # #                 "PrId": project,
# # #                 "ItId": item,
# # #                 "Qu": 8.0,
# # #                 # AFAS sometimes insists on this specific timestamp format
# # #                 "Da": f"{safe_date}T00:00:00" 
# # #             }}}}       
# # #             post_resp = requests.post(f"{BASE_URL}/PtRealization", headers=headers, json=payload)
            
# # #             # 4. SHOW RESULT
# # #             self.send_response(200)
# # #             self.send_header('Content-type', 'text/html; charset=utf-8')
# # #             self.end_headers()
            
# # #             if post_resp.status_code in [200, 201]:
# # #                 html = f"""
# # #                 <html><body style="text-align:center; font-family:sans-serif; padding-top:100px; background-color:#f0fdf4;">
# # #                     <h1 style="color:#166534; font-size:60px;">✅ SUCCESS!</h1>
# # #                     <p style="font-size:24px;">The Banana is yours! Cloned to {safe_date}.</p>
# # #                 </body></html>
# # #                 """
# # #             else:
# # #                 html = f"""
# # #                 <html><body style="text-align:center; font-family:sans-serif; padding-top:100px; background-color:#fef2f2;">
# # #                     <h1 style="color:#991b1b; font-size:60px;">❌ FAILED</h1>
# # #                     <p>AFAS said: {post_resp.text}</p>
# # #                 </body></html>
# # #                 """
# # #             self.wfile.write(html.encode('utf-8'))

# # #         except Exception as e:
# # #             self.send_response(200)
# # #             self.end_headers()
# # #             self.wfile.write(f"Error: {str(e)}".encode())
            
# # # # from http.server import BaseHTTPRequestHandler
# # # # import base64, requests, json
# # # # from datetime import datetime

# # # # # --- CONFIGURATION ---
# # # # AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
# # # # BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices/connectors"

# # # # class handler(BaseHTTPRequestHandler):
# # # #     def do_GET(self):
# # # #         token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
# # # #         headers = {'Authorization': f'AfasToken {token}', 'Content-Type': 'application/json'}

# # # #         # Automatically get TODAY'S date in the YYYY-MM-DD format AFAS requires
# # # #         today_date = datetime.now().strftime("%Y-%m-%d")

# # # #         try:
# # # #             # CLONE: Using your real ID 1000994 and TODAY'S date
# # # #             payload = {"PtRealization": {"Element": {"Fields": {
# # # #                 "EmId": "1000994",      # Your verified ID
# # # #                 "PrId": "VV",           # Project 'VV'
# # # #                 "ItId": "VZ",           # Itemcode 'VZ'
# # # #                 "Qu": 8.0,
# # # #                 "Da": today_date        # Dynamic date for today
# # # #             }}}}
            
# # # #             post_resp = requests.post(f"{BASE_URL}/PtRealization", headers=headers, json=payload)
            
# # # #             self.send_response(200)
# # # #             self.send_header('Content-type', 'text/html; charset=utf-8')
# # # #             self.end_headers()
            
# # # #             if post_resp.status_code in [200, 201]:
# # # #                 html = f"""
# # # #                 <html>
# # # #                 <body style="text-align:center; font-family:sans-serif; padding-top:100px; background-color:#f0fdf4;">
# # # #                     <h1 style="color:#166534; font-size:60px;">✅ SUCCESS!</h1>
# # # #                     <p style="font-size:24px;">Winnie, you did it! Entry created for {today_date}.</p>
# # # #                 </body>
# # # #                 </html>
# # # #                 """
# # # #             else:
# # # #                 # Displays the error clearly so we can troubleshoot further if needed
# # # #                 html = f"""
# # # #                 <html>
# # # #                 <body style="text-align:center; font-family:sans-serif; padding-top:100px; background-color:#fef2f2;">
# # # #                     <h1 style="color:#991b1b; font-size:60px;">❌ FAILED</h1>
# # # #                     <p style="font-size:20px;">AFAS rejected the entry for {today_date}:</p>
# # # #                     <code style="background:#fff; padding:10px; border:1px solid #fecaca;">{post_resp.text}</code>
# # # #                 </body>
# # # #                 </html>
# # # #                 """
# # # #             self.wfile.write(html.encode('utf-8'))

# # # #         except Exception as e:
# # # #             self.send_response(200)
# # # #             self.end_headers()
# # # #             self.wfile.write(f"Error: {str(e)}".encode())


# # # # # from http.server import BaseHTTPRequestHandler
# # # # # import base64, requests, json, datetime
# # # # # from urllib.parse import urlparse, parse_qs

# # # # # # --- CONFIGURATION ---
# # # # # AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
# # # # # BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices/connectors"

# # # # # class handler(BaseHTTPRequestHandler):
# # # # #     def do_GET(self):
# # # # #         query = parse_qs(urlparse(self.path).query)
# # # # #         user_id = query.get('user_id', [None])[0]
        
# # # # #         token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
# # # # #         headers = {'Authorization': f'AfasToken {token}', 'Content-Type': 'application/json'}

# # # # #         try:
# # # # #             # --- NEW: VALIDATION STEP ---
# # # # #             # Check if this employee exists and is active
# # # # #             emp_resp = requests.get(f"{BASE_URL}/Profit_Employee?filterfieldids=EmployeeId&filtervalues={user_id}&operatortypes=1", headers=headers)
# # # # #             emp_data = emp_resp.json().get('rows', [])
            
# # # # #             is_active = False
# # # # #             suggested_id = None

# # # # #             if emp_data:
# # # # #                 # If they have an 'EndDate' (or similar), they might be out of service
# # # # #                 # Adjust 'EmploymentEnd' based on your actual AFAS Connector field name
# # # # #                 end_date = emp_data[0].get('EmploymentEnd')
# # # # #                 if not end_date or datetime.datetime.strptime(end_date, "%Y-%m-%d") > datetime.datetime.now():
# # # # #                     is_active = True
            
# # # # #             # If not active, find a "live" one to suggest (Top 1 active)
# # # # #             if not is_active:
# # # # #                 suggest_resp = requests.get(f"{BASE_URL}/Profit_Employee?take=1", headers=headers)
# # # # #                 suggestions = suggest_resp.json().get('rows', [])
# # # # #                 if suggestions:
# # # # #                     suggested_id = suggestions[0].get('EmployeeId')

# # # # #             # --- ORIGINAL LOGIC (Only if active) ---
# # # # #             success_count = 0
# # # # #             error_details = []
# # # # #             today = datetime.datetime.now().strftime("%Y-%m-%d")

# # # # #             if is_active:
# # # # #                 afas_resp = requests.get(f"{BASE_URL}/Profit_Realization", headers=headers)
# # # # #                 all_rows = afas_resp.json().get('rows', [])
# # # # #                 my_rows = [r for r in all_rows if str(r.get('EmployeeId')) == str(user_id)]
                
# # # # #                 for row in my_rows:
# # # # #                     payload = {
# # # # #                         "PtRealization": {
# # # # #                             "Element": {
# # # # #                                 "Fields": {
# # # # #                                     "EmId": row.get('EmployeeId'),
# # # # #                                     "PrId": row.get('ProjectID'),
# # # # #                                     "ItId": row.get('ItemCodeId'),
# # # # #                                     "UnId": row.get('UnitId'),
# # # # #                                     "Qu": row.get('QuantityUnit'),
# # # # #                                     "Da": today 
# # # # #                                 }
# # # # #                             }
# # # # #                         }
# # # # #                     }
# # # # #                     post_resp = requests.post(f"{BASE_URL}/PtRealization", headers=headers, json=payload)
# # # # #                     if post_resp.status_code in [200, 201]:
# # # # #                         success_count += 1
# # # # #                     else:
# # # # #                         error_details.append(post_resp.json().get('externalMessage', 'Unknown Error'))

# # # # #             # --- DYNAMIC HTML RESPONSE ---
# # # # #             self.send_response(200)
# # # # #             self.send_header('Content-type', 'text/html; charset=utf-8')
# # # # #             self.end_headers()
            
# # # # #             status_color = "#0070f3" if is_active else "#ff4d4d"
# # # # #             status_msg = "✅ Active Employee Found" if is_active else "⚠️ Employee Out of Service"
            
# # # # #             html = f"""
# # # # #             <html><body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
# # # # #                 <h1 style="color: {status_color};">{status_msg}</h1>
# # # # #                 <p>Checking ID: <b>{user_id}</b></p>
# # # # #             """
            
# # # # #             if not is_active and suggested_id:
# # # # #                 html += f"""
# # # # #                 <div style="background: #fff5f5; border: 1px solid #ff4d4d; display: inline-block; padding: 20px; border-radius: 8px;">
# # # # #                     <p>Employee <b>{user_id}</b> is no longer with us.</p>
# # # # #                     <p>Try testing with an active ID like: <a href="?user_id={suggested_id}"><b>{suggested_id}</b></a></p>
# # # # #                 </div>
# # # # #                 """
# # # # #             elif is_active:
# # # # #                 html += f"<p>Processed <b>{success_count}</b> entries.</p>"
# # # # #                 if error_details:
# # # # #                     html += f'<p style="color:red"><b>AFAS Error:</b> {error_details[0]}</p>'

# # # # #             html += "</body></html>"
# # # # #             self.wfile.write(html.encode('utf-8'))

# # # # #         except Exception as e:
# # # # #             self.send_response(500)
# # # # #             self.end_headers()
# # # # #             self.wfile.write(str(e).encode())

# # # # # # from http.server import BaseHTTPRequestHandler
# # # # # # import base64, requests, json, datetime
# # # # # # from urllib.parse import urlparse, parse_qs

# # # # # # # --- CONFIGURATION ---
# # # # # # AFAS_TOKEN_XML = "<token><version>1</version><data>1B1A038E744849258476AB929131EE04E5A54C3706484C6394A850E686E56116</data></token>"
# # # # # # BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices/connectors"

# # # # # # class handler(BaseHTTPRequestHandler):
# # # # # #     def do_GET(self):
# # # # # #         query = parse_qs(urlparse(self.path).query)
# # # # # #         user_id = query.get('user_id', [None])[0]
        
# # # # # #         token = base64.b64encode(AFAS_TOKEN_XML.encode()).decode()
# # # # # #         headers = {'Authorization': f'AfasToken {token}', 'Content-Type': 'application/json'}

# # # # # #         try:
# # # # # #             # 1. Fetch the rows
# # # # # #             afas_resp = requests.get(f"{BASE_URL}/Profit_Realization", headers=headers)
# # # # # #             all_rows = afas_resp.json().get('rows', [])
# # # # # #             my_rows = [r for r in all_rows if str(r.get('EmployeeId')) == str(user_id)]
            
# # # # # #             # 2. Get Today's Date in AFAS format (YYYY-MM-DD)
# # # # # #             today = datetime.datetime.now().strftime("%Y-%m-%d")
            
# # # # # #             success_count = 0
# # # # # #             error_details = []

# # # # # #             # 3. Push to AFAS with the Date Fix
# # # # # #             for row in my_rows:
# # # # # #                 payload = {
# # # # # #                     "PtRealization": {
# # # # # #                         "Element": {
# # # # # #                             "Fields": {
# # # # # #                                 "EmId": row.get('EmployeeId'),
# # # # # #                                 "PrId": row.get('ProjectID'),
# # # # # #                                 "ItId": row.get('ItemCodeId'),
# # # # # #                                 "UnId": row.get('UnitId'),
# # # # # #                                 "Qu": row.get('QuantityUnit'),
# # # # # #                                 "Da": today  # FIX: Using today's date instead of 2020!
# # # # # #                             }
# # # # # #                         }
# # # # # #                     }
# # # # # #                 }
                
# # # # # #                 post_resp = requests.post(f"{BASE_URL}/PtRealization", headers=headers, json=payload)
# # # # # #                 if post_resp.status_code in [200, 201]:
# # # # # #                     success_count += 1
# # # # # #                 else:
# # # # # #                     error_details.append(post_resp.json().get('externalMessage', 'Unknown Error'))

# # # # # #             # 4. Final Success Page
# # # # # #             self.send_response(200)
# # # # # #             self.send_header('Content-type', 'text/html; charset=utf-8')
# # # # # #             self.end_headers()
            
# # # # # #             html = f"""
# # # # # #             <html><body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
# # # # # #                 <h1 style="color: #0070f3;">{'✅ Success!' if success_count > 0 else '❌ Action Needed'}</h1>
# # # # # #                 <p style="font-size: 1.2em;">Processed <b>{success_count}</b> entries for Employee <b>{user_id}</b>.</p>
# # # # # #                 {f'<p style="color:red"><b>AFAS says:</b> {error_details[0]}</p>' if error_details else ''}
# # # # # #                 <p style="color: #666;">Entries were sent with date: {today}</p>
# # # # # #             </body></html>
# # # # # #             """
# # # # # #             self.wfile.write(html.encode('utf-8'))

# # # # # #         except Exception as e:
# # # # # #             self.send_response(500)
# # # # # #             self.end_headers()
# # # # # #             self.wfile.write(str(e).encode())


# # # # # # # from http.server import BaseHTTPRequestHandler
# # # # # # # import json
# # # # # # # from urllib.parse import urlparse, parse_qs

# # # # # # # class handler(BaseHTTPRequestHandler):
# # # # # # #     def do_GET(self):
# # # # # # #         query = parse_qs(urlparse(self.path).query)
# # # # # # #         user_id = query.get('user_id', ['Unknown'])[0]

# # # # # # #         self.send_response(200)
# # # # # # #         # Added charset=utf-8 to fix the funny characters!
# # # # # # #         self.send_header('Content-type', 'text/html; charset=utf-8') 
# # # # # # #         self.end_headers()
        
# # # # # # #         success_page = f"""
# # # # # # #         <html>
# # # # # # #             <head><meta charset="UTF-8"></head>
# # # # # # #             <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
# # # # # # #                 <h1 style="color: #0070f3;">✅ Success!</h1>
# # # # # # #                 <p style="font-size: 1.2em;">Hours for Employee <b>{user_id}</b> have been processed in AFAS 90114.</p>
# # # # # # #                 <p style="color: #666;">You can safely close this window now.</p>
# # # # # # #             </body>
# # # # # # #         </html>
# # # # # # #         """
# # # # # # #         self.wfile.write(success_page.encode('utf-8'))

# # # # # # # # from http.server import BaseHTTPRequestHandler
# # # # # # # # import json
# # # # # # # # from urllib.parse import urlparse, parse_qs

# # # # # # # # class handler(BaseHTTPRequestHandler):
# # # # # # # #     def do_GET(self):
# # # # # # # #         # 1. Parse the User ID from the URL
# # # # # # # #         query = parse_qs(urlparse(self.path).query)
# # # # # # # #         user_id = query.get('user_id', ['Unknown'])[0]

# # # # # # # #         self.send_response(200)
# # # # # # # #         self.send_header('Content-type', 'text/html')
# # # # # # # #         self.end_headers()
        
# # # # # # # #         # 2. Show a nice success message
# # # # # # # #         success_page = f"""
# # # # # # # #         <html><body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
# # # # # # # #             <h1 style="color: #0070f3;">✅ Success!</h1>
# # # # # # # #             <p>Hours for Employee <b>{user_id}</b> have been processed in AFAS 90114.</p>
# # # # # # # #             <p>You can close this window now.</p>
# # # # # # # #         </body></html>
# # # # # # # #         """
# # # # # # # #         self.wfile.write(success_page.encode())


# # # # # # # # # from http.server import BaseHTTPRequestHandler
# # # # # # # # # from urllib.parse import urlparse, parse_qs
# # # # # # # # # import json
# # # # # # # # # # Import your logic from the file we named earlier
# # # # # # # # # from post_hours_for_employee import post_hours, get_auth_header 

# # # # # # # # # class handler(BaseHTTPRequestHandler):
# # # # # # # # #     def do_GET(self):
# # # # # # # # #         # 1. Parse the user_id from the URL link
# # # # # # # # #         query_components = parse_qs(urlparse(self.path).query)
# # # # # # # # #         user_id = query_components.get("user_id", [None])[0]

# # # # # # # # #         if not user_id:
# # # # # # # # #             self.send_response(400)
# # # # # # # # #             self.end_headers()
# # # # # # # # #             self.wfile.write(b"Error: No User ID provided.")
# # # # # # # # #             return

# # # # # # # # #         # 2. Logic: In a real app, you'd fetch the saved hours from a DB here.
# # # # # # # # #         # For this example, let's assume we have the hours ready to go.
# # # # # # # # #         # This calls your AFAS UpdateConnector logic
# # # # # # # # #         dummy_hours = [{"Project": "1001", "Aantal": 8.0, "Toelichting": "Copied via Email"}]
# # # # # # # # #         result = post_hours(user_id, dummy_hours)

# # # # # # # # #         # 3. Respond to the employee in the browser
# # # # # # # # #         self.send_response(200)
# # # # # # # # #         self.send_header('Content-type', 'text/html')
# # # # # # # # #         self.end_headers()
        
# # # # # # # # #         response_html = f"""
# # # # # # # # #         <html>
# # # # # # # # #             <body style="font-family: sans-serif; text-align: center; padding: 50px;">
# # # # # # # # #                 <h1>✅ Success!</h1>
# # # # # # # # #                 <p>Hi {user_id}, your hours have been copied to AFAS environment 90114.</p>
# # # # # # # # #                 <p>Processed {result['success']} entries.</p>
# # # # # # # # #             </body>
# # # # # # # # #         </html>
# # # # # # # # #         """
# # # # # # # # #         self.wfile.write(response_html.encode())
