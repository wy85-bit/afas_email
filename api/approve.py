from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Parse the User ID from the URL
        query = parse_qs(urlparse(self.path).query)
        user_id = query.get('user_id', ['Unknown'])[0]

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # 2. Show a nice success message
        success_page = f"""
        <html><body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
            <h1 style="color: #0070f3;">✅ Success!</h1>
            <p>Hours for Employee <b>{user_id}</b> have been processed in AFAS 90114.</p>
            <p>You can close this window now.</p>
        </body></html>
        """
        self.wfile.write(success_page.encode())


# from http.server import BaseHTTPRequestHandler
# from urllib.parse import urlparse, parse_qs
# import json
# # Import your logic from the file we named earlier
# from post_hours_for_employee import post_hours, get_auth_header 

# class handler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         # 1. Parse the user_id from the URL link
#         query_components = parse_qs(urlparse(self.path).query)
#         user_id = query_components.get("user_id", [None])[0]

#         if not user_id:
#             self.send_response(400)
#             self.end_headers()
#             self.wfile.write(b"Error: No User ID provided.")
#             return

#         # 2. Logic: In a real app, you'd fetch the saved hours from a DB here.
#         # For this example, let's assume we have the hours ready to go.
#         # This calls your AFAS UpdateConnector logic
#         dummy_hours = [{"Project": "1001", "Aantal": 8.0, "Toelichting": "Copied via Email"}]
#         result = post_hours(user_id, dummy_hours)

#         # 3. Respond to the employee in the browser
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()
        
#         response_html = f"""
#         <html>
#             <body style="font-family: sans-serif; text-align: center; padding: 50px;">
#                 <h1>✅ Success!</h1>
#                 <p>Hi {user_id}, your hours have been copied to AFAS environment 90114.</p>
#                 <p>Processed {result['success']} entries.</p>
#             </body>
#         </html>
#         """
#         self.wfile.write(response_html.encode())
