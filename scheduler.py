# v3-cloud/scheduler.py
# Determine which problems are due for review today based on spaced repetition schedule

from datetime import datetime, timedelta
from collections import defaultdict
from sheet_fetch import fetch_all_users_data

REVIEW_INTERVALS = {
    1: 1,
    2: 3,
    3: 7,
    4: 14,
    5: 30
}

def compute_next_review_dates(entries):
    review_map = defaultdict(list)
    for entry in entries:
        user = entry["user_email"]
        key = (user, entry["Problem"].strip())
        review_map[key].append(entry)
    
    tasks = []
    today = datetime.today().date()
    for (user, problem), records in review_map.items():
        # sort by solved date
        records = sorted(records, key=lambda x: x["Solved Date"])
        solved_date = datetime.strptime(records[0]["Solved Date"], "%Y-%m-%d").date()
        current_round = len(records)
        if current_round + 1 not in REVIEW_INTERVALS:
            continue
        next_day = solved_date + timedelta(days=sum([REVIEW_INTERVALS[r] for r in range(1, current_round + 1)]))
        if next_day == today:
            tasks.append({
                "user_email": user,
                "Problem": problem,
                "URL": records[0].get("URL", ""),
                "Round": current_round + 1,
                "Solved Date": solved_date.strftime("%Y-%m-%d")
            })
    return tasks

if __name__ == "__main__":
    all_entries = fetch_all_users_data()
    due = compute_next_review_dates(all_entries)
    print(f"📆 {len(due)} tasks due today:")
    for task in due:
        print(f"- {task['user_email']}: {task['Problem']} (Round {task['Round']})")