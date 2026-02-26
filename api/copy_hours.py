import os
import sys
import requests
from datetime import datetime, timedelta

# Config from your original script
AFAS_TOKEN = os.getenv("AFAS_TOKEN", '5BA4B542D3654105BCDB197D8FE4A23C') # Safely pulled from GitHub Secrets
AFAS_BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

def sync_hours(user_id):
    headers = {'Authorization': f'AfasToken {AFAS_TOKEN}', 'Content-Type': 'application/json'}
    try:
        print(f"Starting sync for {user_id}...")
        today = datetime.now()
        last_mon = (today - timedelta(days=today.weekday() + 7)).strftime('%Y-%m-%d')
        last_sun = (today - timedelta(days=today.weekday() + 1)).strftime('%Y-%m-%d')

        # 1. Fetch last week's data
        get_url = f"{AFAS_BASE_URL}/connectors/Profit_Realization?filterfieldids=EmployeeId,DateTime&filtervalues={user_id},{last_mon};{last_sun}&operatortypes=1,9"
        source_data = requests.get(get_url, headers=headers).json().get('rows', [])

        if not source_data:
            print(f"No hours found for {user_id} between {last_mon} and {last_sun}.")
            return

        # 2. Copy to this week
        for entry in source_data:
            new_date = (datetime.strptime(entry['Da'], '%Y-%m-%d') + timedelta(days=7)).strftime('%Y-%m-%d')
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
            res = requests.post(f"{AFAS_BASE_URL}/connectors/PtRealization", json=payload, headers=headers)
            print(f"Sent entry for {new_date}: Status {res.status_code}")

        print(f"✅ [{user_id}] Sync complete.")

    except Exception as e:
        print(f"❌ [{user_id}] Sync error: {e}")

if __name__ == "__main__":
    # Get user_id from GitHub Action payload
    if len(sys.argv) > 2 and sys.argv[1] == '--user':
        target_user = sys.argv[2]
        sync_hours(target_user)
    else:
        print("No user provided to script.")
