# send_reminders.py
# Send email reminders to users for problems due today

import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from scheduler import compute_next_review_dates
from sheet_fetch import fetch_all_users_data


print("🔥 ReCurve Reminder Service is running on Railway")

load_dotenv(dotenv_path="config/config.env")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
print("📧 DEBUG EMAIL:", EMAIL_ADDRESS, EMAIL_PASSWORD)
FROM_NAME = os.getenv("FROM_NAME", "ReCurve Reminder")

def send_email(to, subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{FROM_NAME} <{EMAIL_ADDRESS}>"
    msg["To"] = to
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def format_email(problem, url, round_num):
    return f"""
Hi there 👋

It's time to review: {problem} (Round {round_num})

🔗 {url}

Once you finish, click this link to mark as reviewed:
[Mark Completed](https://recurve.up.railway.app/mark?problem={problem}&round={round_num})

📊 View your full dashboard here: https://recurve.up.railway.app/dashboard/user@example.com

- ReCurve Team
"""

if __name__ == "__main__":
    print("📬 Sending reminders...")
    tasks = compute_next_review_dates(fetch_all_users_data())
    if not tasks:
        print("✅ No reviews due today.")
    for task in tasks:
        email = task["user_email"]
        problem = task["Problem"]
        url = task["URL"]
        round_num = task["Round"]
        body = format_email(problem, url, round_num)
        send_email(email, f"ReCurve ⏰ Review {problem} (Round {round_num})", body)
        print(f"✅ Sent: {problem} (Round {round_num}) to {email}")