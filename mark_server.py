# v3-cloud/mark_server.py
# Simple Flask server to handle 'mark as reviewed' clicks

from flask import Flask, request, jsonify, render_template_string
import csv
import os
from datetime import datetime

app = Flask(__name__)

REVIEW_LOG = "v3-cloud/review_log.csv"

def log_review(email, problem, round_num):
    os.makedirs(os.path.dirname(REVIEW_LOG), exist_ok=True)
    reviewed_at = datetime.now().isoformat()
    with open(REVIEW_LOG, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([email, problem, round_num, reviewed_at])

@app.route("/mark", methods=["GET"])
def mark():
    email = request.args.get("email")
    problem = request.args.get("problem")
    round_num = request.args.get("round")

    if not (email and problem and round_num):
        return "❌ Missing parameters.", 400

    log_review(email, problem, round_num)
    return render_template_string("""
    <html>
        <head><title>✅ Review Logged</title></head>
        <body style="font-family: sans-serif; text-align: center; margin-top: 50px;">
            <h1>✅ Review Recorded</h1>
            <p>{{ problem }} (Round {{ round_num }}) marked as completed for {{ email }}.</p>
        </body>
    </html>
    """, email=email, problem=problem, round_num=round_num)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)