import os
import sys
import requests
from datetime import datetime, timedelta

# --- CONFIG ---
# Pulling the token from GitHub Secrets for security
AFAS_TOKEN = os.getenv("AFAS_TOKEN")
AFAS_BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

def sync_hours(user_id):
    """Copies hours for a specific user from last week to the current week."""
    
    # Validation: Ensure we actually have a token
    if not AFAS_TOKEN:
        print("❌ Error: AFAS_TOKEN environment variable is missing!")
        return

    headers = {
        'Authorization': f'AfasToken {AFAS_TOKEN}',
        'Content-Type': 'application/json'
    }

    try:
        # Calculate Dates
        today = datetime.now()
        # Last Monday
        last_mon = (today - timedelta(days=today.weekday() + 7)).strftime('%Y-%m-%d')
        # Last Sunday
        last_sun = (today - timedelta(days=today.weekday() + 1)).strftime('%Y-%m-%d')

        print(f"🚀 Starting sync for User ID: {user_id}")
        print(f"📅 Looking for hours between {last_mon} and {last_sun}...")

        # 1. FETCH DATA
        get_url = f"{AFAS_BASE_URL}/connectors/Profit_Realization?filterfieldids=EmployeeId,DateTime&filtervalues={user_id},{last_mon};{last_sun}&operatortypes=1,9"

        print(f"Token starts with: {AFAS_TOKEN[:5]}... and ends with: {AFAS_TOKEN[-5:]}")
        response = requests.get(get_url, headers=headers)

        # Check if the GET request worked
        if response.status_code != 200:
            print(f"❌ AFAS GET Error ({response.status_code}): {response.text}")
            return

        # Try to parse JSON safely
        try:
            source_data = response.json().get('rows', [])
        except ValueError:
            print("❌ Failed to decode JSON. AFAS sent back something else:")
            print(response.text)
            return

        if not source_data:
            print(f"ℹ️ No hours found for {user_id} in the previous week.")
            return

        print(f"✅ Found {len(source_data)} entries. Copying to current week...")

        # 2. POST DATA (COPYING)
        for entry in source_data:
            # Shift the date forward by 7 days
            original_date = datetime.strptime(entry['Da'], '%Y-%m-%d')
            new_date = (original_date + timedelta(days=7)).strftime('%Y-%m-%d')
            
            payload = {
                "PtRealization": {
                    "Element": {
                        "Fields": {
                            "DaTi": new_date,
                            "EmId": user_id,
                            "PrId": entry.get('PrId', '82'),
                            "StTi": entry.get('StTi', '09:00:00'),
                            "EnTi": entry.get('EnTi', '17:00:00'),
                            "Ap": True,
                            "Pr": True
                        }
                    }
                }
            }
            
            post_res = requests.post(f"{AFAS_BASE_URL}/connectors/PtRealization", json=payload, headers=headers)
            
            if post_res.status_code in [200, 201, 204]:
                print(f"✔️ Successfully copied entry for {new_date}")
            else:
                print(f"⚠️ Failed to copy entry for {new_date}: {post_res.text}")

        print(f"🎉 Process finished for {user_id}!")

    except Exception as e:
        print(f"❌ Unexpected Script Error: {e}")

if __name__ == "__main__":
    # This part reads the '--user 90114' part from your GitHub Action
    if len(sys.argv) > 2 and sys.argv[1] == '--user':
        target_user = sys.argv[2]
        sync_hours(target_user)
    else:
        print("❌ Error: No User ID provided in command line arguments.")


# import os
# import sys
# import requests
# from datetime import datetime, timedelta

# # Config from your original script
# AFAS_TOKEN = os.getenv("AFAS_TOKEN", '5BA4B542D3654105BCDB197D8FE4A23C') # Safely pulled from GitHub Secrets
# AFAS_BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

# def sync_hours(user_id):
#     headers = {'Authorization': f'AfasToken {AFAS_TOKEN}', 'Content-Type': 'application/json'}
#     try:
#         print(f"Starting sync for {user_id}...")
#         today = datetime.now()
#         last_mon = (today - timedelta(days=today.weekday() + 7)).strftime('%Y-%m-%d')
#         last_sun = (today - timedelta(days=today.weekday() + 1)).strftime('%Y-%m-%d')

#         # 1. Fetch last week's data
#         get_url = f"{AFAS_BASE_URL}/connectors/Profit_Realization?filterfieldids=EmployeeId,DateTime&filtervalues={user_id},{last_mon};{last_sun}&operatortypes=1,9"
#         source_data = requests.get(get_url, headers=headers).json().get('rows', [])

#         if not source_data:
#             print(f"No hours found for {user_id} between {last_mon} and {last_sun}.")
#             return

#         # 2. Copy to this week
#         for entry in source_data:
#             new_date = (datetime.strptime(entry['Da'], '%Y-%m-%d') + timedelta(days=7)).strftime('%Y-%m-%d')
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
#             res = requests.post(f"{AFAS_BASE_URL}/connectors/PtRealization", json=payload, headers=headers)
#             print(f"Sent entry for {new_date}: Status {res.status_code}")

#         print(f"✅ [{user_id}] Sync complete.")

#     except Exception as e:
#         print(f"❌ [{user_id}] Sync error: {e}")

# if __name__ == "__main__":
#     # Get user_id from GitHub Action payload
#     if len(sys.argv) > 2 and sys.argv[1] == '--user':
#         target_user = sys.argv[2]
#         sync_hours(target_user)
#     else:
#         print("No user provided to script.")
