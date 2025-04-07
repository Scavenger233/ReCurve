# sheet_fetch.py
# Fetch simplified user logs from individual Google Sheets using service account credentials

import os
import pandas as pd
import gspread
import json
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path="config/config.env")

def fetch_sheet_data(sheet_id):
    """
    Given a sheet ID, return a list of problem logs as dicts
    """
    try:
        creds_info = json.loads(os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"))
        scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
        gc = gspread.authorize(creds)
        sh = gc.open_by_key(sheet_id)
        worksheet = sh.worksheet("Sheet1")

        all_values = worksheet.get_all_values()
        print("📋 Raw values from sheet:")
        for row in all_values:
            print(row)

        rows = worksheet.get_all_records()
        print(f"📄 Sheet contains {len(rows)} records")
        return rows

    except Exception as e:
        import traceback
        print("❌ Exception during sheet fetch:\n" + traceback.format_exc())
        return []

def fetch_all_users_data(registry_file="user_registry.csv"):
    """
    For each user listed in user_registry.csv, fetch their problem entries
    """
    df = pd.read_csv(registry_file)
    all_data = []
    for _, row in df.iterrows():
        user_email = row["email"]
        sheet_id = row["sheet_id"]
        try:
            user_rows = fetch_sheet_data(sheet_id)
            for entry in user_rows:
                # Skip rows with no Problem or Solved Date
                if not entry.get("Problem") or not entry.get("Solved Date"):
                    continue
                entry["user_email"] = user_email
                all_data.append(entry)
        except Exception as e:
            print(f"❌ Failed to fetch for {user_email}: {e}")
    return all_data

if __name__ == "__main__":
    from pprint import pprint
    pprint(fetch_all_users_data())