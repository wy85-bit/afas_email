import sys
import os
import requests # You'll likely need this for AFAS

def main():
    # 1. Get the user from the command line (passed by GitHub Action)
    if len(sys.argv) < 3 or sys.argv[1] != '--user':
        print("Error: No user provided.")
        return
    
    user_id = sys.argv[2]
    print(f"🚀 Starting work for user: {user_id}")

    # 2. Get your AFAS credentials from environment variables
    # (We will set these up in GitHub Secrets later)
    afas_token = os.getenv("AFAS_TOKEN")
    
    if not afas_token:
        print("❌ Error: AFAS_TOKEN not found in environment!")
        return

    # --- YOUR AFAS LOGIC GOES HERE ---
    print(f"Connecting to AFAS for {user_id}...")
    
    # Example:
    # response = requests.get(f"https://your-afas-url.com/api/{user_id}", headers=...)
    
    print(f"✅ Successfully copied hours from last week to this week for {user_id}!")

if __name__ == "__main__":
    main()
