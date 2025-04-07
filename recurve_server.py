from flask import Flask, request, render_template
import pandas as pd
import gspread
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv("config/config.env")
EMAIL = os.getenv("EMAIL_ADDRESS")
SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
REVIEW_LOG = "review_log.csv"

# Setup Flask
app = Flask(__name__, template_folder="dashboard/templates", static_folder="dashboard/static")

# Get sheet_id from user_registry
def get_sheet_id(email):
    df = pd.read_csv("user_registry.csv")
    user_row = df[df['email'] == email]
    if not user_row.empty:
        return user_row.iloc[0]['sheet_id']
    return None

# Get today's tasks from the sheet
def fetch_today_tasks(sheet_id):
    creds_dict = json.loads(SERVICE_ACCOUNT_JSON)
    gc = gspread.service_account_from_dict(creds_dict)
    sheet = gc.open_by_key(sheet_id).sheet1
    records = sheet.get_all_records()
    today_str = datetime.today().strftime("%Y-%m-%d")
    return [r for r in records if r.get("Next Review Date") == today_str]

# Homepage dashboard
@app.route("/dashboard")
def dashboard():
    email = request.args.get("email")
    if not email:
        return "❌ Please provide ?email=... in the URL"

    sheet_id = get_sheet_id(email)
    if not sheet_id:
        return f"❌ No sheet registered for {email}"

    try:
        tasks = fetch_today_tasks(sheet_id)
    except Exception as e:
        return f"❌ Error fetching tasks: {str(e)}"

    return render_template("index.html", tasks=tasks, email=email)

# Click to mark reviewed
@app.route("/mark_reviewed")
def mark_reviewed():
    email = request.args.get("email")
    problem = request.args.get("problem")
    round_num = request.args.get("round")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not all([email, problem, round_num]):
        return "❌ Missing parameters"

    log_row = f"{ts},{email},{problem},{round_num}\n"
    with open(REVIEW_LOG, "a") as f:
        f.write(log_row)

    return f"✅ Marked as reviewed: {problem} Round {round_num} for {email}"

if __name__ == "__main__":
    app.run(debug=True, port=8080)