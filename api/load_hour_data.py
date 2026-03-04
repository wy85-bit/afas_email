import base64
import requests
import json

# --- CONFIGURATION ---
API_KEY = "5BA4B542D3654105BCDB197D8FE4A23C"
ENV_KEY = "E4E4E336283D4A69891CA03BE85D4A57"
BASE_URL = "https://90114.resttest.afas.online/ProfitRestServices"

def get_afas_headers():
    """Constructs the Base64 token header that AFAS requires."""
    # The 'Wrapped' format we verified earlier
    raw_token = f"<token>{API_KEY}{ENV_KEY}</token>"
    encoded_token = base64.b64encode(raw_token.encode('utf-8')).decode('utf-8')
    return {
        'Authorization': f'AfasToken {encoded_token}',
        'Content-Type': 'application/json'
    }

def download_all_employee_hours():
    """
    Downloads every hour record available to the TestWinnie connector.
    Organizes them by Employee ID for easy individual processing.
    """
    headers = get_afas_headers()
    # Using the Profit_Realization GetConnector
    url = f"{BASE_URL}/connectors/Profit_Realization"
    
    print("🛰️ Connecting to AFAS environment 90114...")
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            rows = data.get('rows', [])
            print(f"✅ Successfully retrieved {len(rows)} total records.")
            
            # Group records by Employee ID (Medewerker)
            grouped_data = {}
            for row in rows:
                emp_id = row.get('Medewerker') # This is the ID like 90114
                
                if emp_id not in grouped_data:
                    grouped_data[emp_id] = {
                        "name": row.get('Naam', 'Unknown'),
                        "email": row.get('Email', None), # Requires 'Email' field in GetConnector
                        "hours_to_copy": []
                    }
                
                grouped_data[emp_id]["hours_to_copy"].append({
                    "project": row.get('Project'),
                    "description": row.get('Toelichting'),
                    "units": row.get('Aantal')
                })
                
            return grouped_data
            
        elif response.status_code == 401:
            print("❌ Unauthorized: Check if user 90114 is still in group PR-006.")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"⚠️ Connection error: {e}")
    
    return {}

if __name__ == "__main__":
    # Test run: Fetch and print a summary
    all_hours = download_all_employee_hours()
    
    for emp_id, info in all_hours.items():
        print(f"👤 {info['name']} ({emp_id}): {len(info['hours_to_copy'])} entries found.")
