import base64
import requests
import json
from datetime import datetime, timedelta

# --- CONFIGURATION ---
# These keys are taken directly from your TestWinnie App Connector
API_KEY = "5BA4B542D3654105BCDB197D8FE4A23C"
ENV_KEY = "E4E4E336283D4A69891CA03BE85D4A57"
AFAS_URL = "https://90114.resttest.afas.online/ProfitRestServices" # Environment 90114

def get_afas_token():
    """Constructs the specific Base64 token AFAS requires."""
    # AFAS expects the keys combined and wrapped in XML-style tags
    raw_token = f"<token>{API_KEY}{ENV_KEY}</token>"
    encoded_token = base64.b64encode(raw_token.encode('utf-8')).decode('utf-8')
    return encoded_token

def sync_hours(user_id):
    print(f"🚀 Starting sync for User ID: {user_id}")
    
    token = get_afas_token()
    headers = {
        'Authorization': f'AfasToken {token}',
        'Content-Type': 'application/json'
    }

    # Example: Fetching from the Profit_Realization GetConnector
    endpoint = f"{AFAS_URL}/connectors/Profit_Realization"
    
    try:
        response = requests.get(endpoint, headers=headers)
        
        if response.status_code == 200:
            print("✅ Success! Connected to AFAS.")
            data = response.json()
            # Here you would add your logic to process the hours
            print(f"Retrieved {len(data.get('rows', []))} records.")
        elif response.status_code == 401:
            print("❌ AFAS Connection Failed (401): Unauthorized.")
            print("Check: Is IP-restricties empty? Is user 90114 still in group PR-006?")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"⚠️ An error occurred: {e}")

if __name__ == "__main__":
    # Using the ID from your user properties
    sync_hours("90114")

# import os
# import sys
# import requests
# from datetime import datetime, timedelta
# import base64

# # --- CONFIG ---
# # Pulling the token from GitHub Secrets
# AFAS_TOKEN = os.getenv("AFAS_TOKEN")
# AFAS_BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

# def sync_hours(user_id):
#     """Copies hours for a specific user from last week to the current week."""
    
#     # 1. AUTHENTICATION (The Base64 "Secret Knock")
#     # We combine the API Key and Environment Key with a colon
#     # Based on your screenshot: 5BA4... : E4E4...
#     # 1. AUTHENTICATION (The "Double-Wrapped" Method)
#     # We combine the keys with a colon, wrap them in <token> tags, THEN encode.
#     import base64
    
#     # Your actual keys from the screenshot
#     api_key = "5BA4B542D3654105BCDB197D8FE4A23C"
#     env_key = "E4E4E336283D4A69891CA03BE85D4A57"

#     # Method: Combined with a colon and wrapped in the <token> tag
#     # This is the "Industry Standard" for AFAS REST services
#     token_content = f"<token>{api_key}{env_key}</token>"

#     # Encode to Base64
#     token_bytes = token_content.encode('utf-8')
#     encoded_token = base64.b64encode(token_bytes).decode('utf-8')

#     # The Header - Ensure there is exactly one space after 'AfasToken'
#     headers = {
#     'Authorization': f'AfasToken {encoded_token}',
#     'Content-Type': 'application/json'
#     }

#     try:
#         # 2. Calculate Date Range
#         today = datetime.now()
#         last_mon = (today - timedelta(days=today.weekday() + 7)).strftime('%Y-%m-%d')
#         last_sun = (today - timedelta(days=today.weekday() + 1)).strftime('%Y-%m-%d')

#         print(f"🚀 Starting sync for User ID: {user_id}")
#         print(f"📅 Last week was: {last_mon} to {last_sun}")
#         print(f"🔐 Auth: Sending Base64 encoded token...")

#         # 3. Fetch last week's entries
#         get_url = (
#             f"{AFAS_BASE_URL}/connectors/Profit_Realization"
#             f"?filterfieldids=EmployeeId,DateTime"
#             f"&filtervalues={user_id},{last_mon};{last_sun}"
#             f"&operatortypes=1,9"
#         )
        
#         response = requests.get(get_url, headers=headers)

#         if response.status_code != 200:
#             print(f"❌ AFAS Connection Failed ({response.status_code})")
#             print(f"Response Body: {response.text}")
#             return

#         source_data = response.json().get('rows', [])

#         if not source_data:
#             print(f"ℹ️ No hours found for {user_id} in the target range.")
#             return

#         print(f"✅ Found {len(source_data)} entries. Beginning copy...")

#         # 4. Post entries to the current week
#         success_count = 0
#         for entry in source_data:
#             original_date = datetime.strptime(entry['Da'], '%Y-%m-%d')
#             new_date = (original_date + timedelta(days=7)).strftime('%Y-%m-%d')
            
#             payload = {
#                 "PtRealization": {
#                     "Element": {
#                         "Fields": {
#                             "DaTi": new_date,
#                             "EmId": user_id,
#                             "PrId": entry.get('PrId', '82'),
#                             "StTi": entry.get('StTi', '09:00:00'),
#                             "EnTi": entry.get('EnTi', '17:00:00'),
#                             "Ap": True,
#                             "Pr": True
#                         }
#                     }
#                 }
#             }
            
#             post_res = requests.post(
#                 f"{AFAS_BASE_URL}/connectors/PtRealization", 
#                 json=payload, 
#                 headers=headers
#             )
            
#             if post_res.status_code in [200, 201, 204]:
#                 print(f"✔️ Copied: {entry.get('PrId', 'Work')} on {new_date}")
#                 success_count += 1
#             else:
#                 print(f"⚠️ Failed to copy entry for {new_date}: {post_res.text}")

#         print(f"🎉 Done! Successfully synced {success_count} entries.")

#     except Exception as e:
#         print(f"❌ Script Error: {e}")

# if __name__ == "__main__":
#     if len(sys.argv) > 2 and sys.argv[1] == '--user':
#         target_user = sys.argv[2]
#         sync_hours(target_user)
#     else:
#         print("❌ Error: No User ID provided.")

# # import os
# # import sys
# # import requests
# # from datetime import datetime, timedelta
# # import base64

# # # --- CONFIG ---
# # AFAS_TOKEN = os.getenv("AFAS_TOKEN")
# # AFAS_BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

# # def sync_hours(user_id):
# #     """Copies hours for a specific user from last week to the current week."""
    
# #     # if not AFAS_TOKEN:
# #     #     print("❌ Error: AFAS_TOKEN environment variable is missing in GitHub Secrets!")
# #     #     return

# #     # Using the specific combined format with a colon
# #     # headers = {
# #     #     'Authorization': f'AfasToken <token>5BA4B542D3654105BCDB197D8FE4A23C:E4E4E336283D4A69891CA03BE85D4A57</token>',
# #     #     'Content-Type': 'application/json'
# #     # }


# #     # 1. Combine the keys with a colon
# #     raw_token = "5BA4B542D3654105BCDB197D8FE4A23C:E4E4E336283D4A69891CA03BE85D4A57"
    
# #     # 2. Base64 encode the combined string
# #     token_bytes = raw_token.encode('utf-8')
# #     encoded_token = base64.b64encode(token_bytes).decode('utf-8')
    
# #     # 3. Send it WITHOUT the <token> tags
# #     headers = {
# #         'Authorization': f'AfasToken {encoded_token}',
# #         'Content-Type': 'application/json'
# #     }
# #     try:
# #         # 1. Calculate Date Range (Last Monday to Last Sunday)
# #         today = datetime.now()
# #         last_mon = (today - timedelta(days=today.weekday() + 7)).strftime('%Y-%m-%d')
# #         last_sun = (today - timedelta(days=today.weekday() + 1)).strftime('%Y-%m-%d')

# #         print(f"🚀 Starting sync for User ID: {user_id}")
# #         print(f"📅 Last week was: {last_mon} to {last_sun}")

# #         # 2. Fetch last week's entries
# #         get_url = (
# #             f"{AFAS_BASE_URL}/connectors/Profit_Realization"
# #             f"?filterfieldids=EmployeeId,DateTime"
# #             f"&filtervalues={user_id},{last_mon};{last_sun}"
# #             f"&operatortypes=1,9"
# #         )
        
# #         print(f"🔗 Requesting data from AFAS...")
# #         response = requests.get(get_url, headers=headers)

# #         if response.status_code != 200:
# #             print(f"❌ AFAS Connection Failed ({response.status_code})")
# #             print(f"Response Body: {response.text}")
# #             return

# #         source_data = response.json().get('rows', [])

# #         if not source_data:
# #             print(f"ℹ️ No hours found for {user_id} in the target range.")
# #             return

# #         print(f"✅ Found {len(source_data)} entries. Beginning copy...")

# #         # 3. Post entries to the current week
# #         success_count = 0
# #         for entry in source_data:
# #             original_date = datetime.strptime(entry['Da'], '%Y-%m-%d')
# #             new_date = (original_date + timedelta(days=7)).strftime('%Y-%m-%d')
            
# #             payload = {
# #                 "PtRealization": {
# #                     "Element": {
# #                         "Fields": {
# #                             "DaTi": new_date,
# #                             "EmId": user_id,
# #                             "PrId": entry.get('PrId', '82'),
# #                             "StTi": entry.get('StTi', '09:00:00'),
# #                             "EnTi": entry.get('EnTi', '17:00:00'),
# #                             "Ap": True,
# #                             "Pr": True
# #                         }
# #                     }
# #                 }
# #             }
            
# #             post_res = requests.post(
# #                 f"{AFAS_BASE_URL}/connectors/PtRealization", 
# #                 json=payload, 
# #                 headers=headers
# #             )
            
# #             if post_res.status_code in [200, 201, 204]:
# #                 print(f"✔️ Copied: {entry.get('PrId', 'Work')} on {new_date}")
# #                 success_count += 1
# #             else:
# #                 print(f"⚠️ Failed to copy entry for {new_date}: {post_res.text}")

# #         print(f"🎉 Done! Successfully synced {success_count} entries for {user_id}.")

# #     except Exception as e:
# #         print(f"❌ Script Error: {e}")

# # if __name__ == "__main__":
# #     if len(sys.argv) > 2 and sys.argv[1] == '--user':
# #         target_user = sys.argv[2]
# #         sync_hours(target_user)
# #     else:
# #         print("❌ Error: No User ID provided. Usage: python copy_hours.py --user <ID>")


# # # import os
# # # import sys
# # # import requests
# # # from datetime import datetime, timedelta

# # # # --- CONFIG ---
# # # # Pulling the token from GitHub Secrets for security
# # # AFAS_TOKEN = os.getenv("AFAS_TOKEN")
# # # AFAS_BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

# # # def sync_hours(user_id):
# # #     """Copies hours for a specific user from last week to the current week."""
    
# # #     # Validation: Ensure we actually have a token
# # #     if not AFAS_TOKEN:
# # #         print("❌ Error: AFAS_TOKEN environment variable is missing!")
# # #         return

# # #     headers = {
# # #         # 'Authorization': f'AfasToken {AFAS_TOKEN}',
# # #         'Authorization': f'AfasToken <token>{AFAS_TOKEN}</token>',
# # #         'Content-Type': 'application/json'
# # #     }

# # #     try:
# # #         # Calculate Dates
# # #         today = datetime.now()
# # #         # Last Monday
# # #         last_mon = (today - timedelta(days=today.weekday() + 7)).strftime('%Y-%m-%d')
# # #         # Last Sunday
# # #         last_sun = (today - timedelta(days=today.weekday() + 1)).strftime('%Y-%m-%d')

# # #         print(f"🚀 Starting sync for User ID: {user_id}")
# # #         print(f"📅 Looking for hours between {last_mon} and {last_sun}...")

# # #         # 1. FETCH DATA
# # #         get_url = f"{AFAS_BASE_URL}/connectors/Profit_Realization?filterfieldids=EmployeeId,DateTime&filtervalues={user_id},{last_mon};{last_sun}&operatortypes=1,9"

# # #         print(f"Token starts with: {AFAS_TOKEN[:5]}... and ends with: {AFAS_TOKEN[-5:]}")
# # #         response = requests.get(get_url, headers=headers)

# # #         # Check if the GET request worked
# # #         if response.status_code != 200:
# # #             print(f"❌ AFAS GET Error ({response.status_code}): {response.text}")
# # #             return

# # #         # Try to parse JSON safely
# # #         try:
# # #             source_data = response.json().get('rows', [])
# # #         except ValueError:
# # #             print("❌ Failed to decode JSON. AFAS sent back something else:")
# # #             print(response.text)
# # #             return

# # #         if not source_data:
# # #             print(f"ℹ️ No hours found for {user_id} in the previous week.")
# # #             return

# # #         print(f"✅ Found {len(source_data)} entries. Copying to current week...")

# # #         # 2. POST DATA (COPYING)
# # #         for entry in source_data:
# # #             # Shift the date forward by 7 days
# # #             original_date = datetime.strptime(entry['Da'], '%Y-%m-%d')
# # #             new_date = (original_date + timedelta(days=7)).strftime('%Y-%m-%d')
            
# # #             payload = {
# # #                 "PtRealization": {
# # #                     "Element": {
# # #                         "Fields": {
# # #                             "DaTi": new_date,
# # #                             "EmId": user_id,
# # #                             "PrId": entry.get('PrId', '82'),
# # #                             "StTi": entry.get('StTi', '09:00:00'),
# # #                             "EnTi": entry.get('EnTi', '17:00:00'),
# # #                             "Ap": True,
# # #                             "Pr": True
# # #                         }
# # #                     }
# # #                 }
# # #             }
            
# # #             post_res = requests.post(f"{AFAS_BASE_URL}/connectors/PtRealization", json=payload, headers=headers)
            
# # #             if post_res.status_code in [200, 201, 204]:
# # #                 print(f"✔️ Successfully copied entry for {new_date}")
# # #             else:
# # #                 print(f"⚠️ Failed to copy entry for {new_date}: {post_res.text}")

# # #         print(f"🎉 Process finished for {user_id}!")

# # #     except Exception as e:
# # #         print(f"❌ Unexpected Script Error: {e}")

# # # if __name__ == "__main__":
# # #     # This part reads the '--user 90114' part from your GitHub Action
# # #     if len(sys.argv) > 2 and sys.argv[1] == '--user':
# # #         target_user = sys.argv[2]
# # #         sync_hours(target_user)
# # #     else:
# # #         print("❌ Error: No User ID provided in command line arguments.")


# # # # import os
# # # # import sys
# # # # import requests
# # # # from datetime import datetime, timedelta

# # # # # Config from your original script
# # # # AFAS_TOKEN = os.getenv("AFAS_TOKEN", '5BA4B542D3654105BCDB197D8FE4A23C') # Safely pulled from GitHub Secrets
# # # # AFAS_BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

# # # # def sync_hours(user_id):
# # # #     headers = {'Authorization': f'AfasToken {AFAS_TOKEN}', 'Content-Type': 'application/json'}
# # # #     try:
# # # #         print(f"Starting sync for {user_id}...")
# # # #         today = datetime.now()
# # # #         last_mon = (today - timedelta(days=today.weekday() + 7)).strftime('%Y-%m-%d')
# # # #         last_sun = (today - timedelta(days=today.weekday() + 1)).strftime('%Y-%m-%d')

# # # #         # 1. Fetch last week's data
# # # #         get_url = f"{AFAS_BASE_URL}/connectors/Profit_Realization?filterfieldids=EmployeeId,DateTime&filtervalues={user_id},{last_mon};{last_sun}&operatortypes=1,9"
# # # #         source_data = requests.get(get_url, headers=headers).json().get('rows', [])

# # # #         if not source_data:
# # # #             print(f"No hours found for {user_id} between {last_mon} and {last_sun}.")
# # # #             return

# # # #         # 2. Copy to this week
# # # #         for entry in source_data:
# # # #             new_date = (datetime.strptime(entry['Da'], '%Y-%m-%d') + timedelta(days=7)).strftime('%Y-%m-%d')
# # # #             payload = {
# # # #                 "PtRealization": {
# # # #                     "Element": {
# # # #                         "Fields": {
# # # #                             "DaTi": new_date, 
# # # #                             "EmId": user_id, 
# # # #                             "PrId": entry.get('PrId', '82'), 
# # # #                             "StTi": entry.get('StTi', '09:00:00'), 
# # # #                             "EnTi": entry.get('EnTi', '17:00:00'), 
# # # #                             "Ap": True, 
# # # #                             "Pr": True
# # # #                         }
# # # #                     }
# # # #                 }
# # # #             }
# # # #             res = requests.post(f"{AFAS_BASE_URL}/connectors/PtRealization", json=payload, headers=headers)
# # # #             print(f"Sent entry for {new_date}: Status {res.status_code}")

# # # #         print(f"✅ [{user_id}] Sync complete.")

# # # #     except Exception as e:
# # # #         print(f"❌ [{user_id}] Sync error: {e}")

# # # # if __name__ == "__main__":
# # # #     # Get user_id from GitHub Action payload
# # # #     if len(sys.argv) > 2 and sys.argv[1] == '--user':
# # # #         target_user = sys.argv[2]
# # # #         sync_hours(target_user)
# # # #     else:
# # # #         print("No user provided to script.")
