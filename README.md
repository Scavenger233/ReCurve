# ReCurve: AI-powered Spaced Repetition for LeetCode

ReCurve helps you retain what you’ve learned by sending personalized review reminders based on **spaced repetition**. Just log your problem-solving in a **Google Sheet**, and ReCurve will take care of the rest.

## 🧠 Why ReCurve?
If you’re tired of forgetting LeetCode problems you’ve already solved, ReCurve is for you. It schedules reviews using a proven memory curve model, and notifies you at the best time to revisit a problem — through **email** or **Telegram** (coming soon).

---

## 🚀 How to Use (For Users)

### Step 1: Copy the Template
Create your own Google Sheet by duplicating this template:
📄 [ReCurve Sheet Template](https://docs.google.com/spreadsheets/d/1pJQVACwd2pbQ5aq4YngFFVWYvSHSI8ilweCzcmH3Mtw/edit?usp=sharing)

### Step 2: Share the Sheet
Click the **Share** button in the top right corner of Google Sheets and add:
```
recurve-sheet-reader@recurvecloud.iam.gserviceaccount.com
```
as a **Viewer**.

That’s it. You’ll start getting email reminders when it’s time to review.

---

## ✍️ How to Fill the Sheet

| Column       | Example                             | Required? |
|--------------|--------------------------------------|-----------|
| Problem      | TwoSum                              | ✅ Yes     |
| URL          | https://leetcode.com/problems/two-sum | ✅ Yes     |
| Solved Date  | 2025-04-05                          | ✅ Yes     |


---

## 📧 Reminder Format
You will receive an email that looks like this:

> **Subject**: ReCurve ⏰ Review TwoSum (Round 2)
> 
> It’s time to review:
> 🔗 https://leetcode.com/problems/two-sum
> 
> ✅ Click here to mark it as reviewed:
> https://your-deployment-url.com/mark?email=youremail@gmail.com&problem=TwoSum&round=2

Once clicked, the system will update your sheet and reschedule the next review.

---

## 🛠️ For Developers
If you want to self-host this system or contribute:

1. Clone this repo
2. Create a `config.env` file based on `.env.example`
3. Add your Google service account credentials JSON
4. Run locally with `python send_reminders.py`

For webhook support, run `python mark_server.py` and deploy to platforms like Railway.

---

## 📄 License
This project is licensed under the **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License**.

You are free to:
- Share — copy and redistribute the material in any medium or format

Under the following terms:
- **Attribution** — You must give appropriate credit.
- **NonCommercial** — You may not use the material for commercial purposes.
- **NoDerivatives** — You may not distribute modified versions.

Full license text: https://creativecommons.org/licenses/by-nc-nd/4.0/

---

Happy coding & spaced repeating!
💡 [Created by Yiming Li](https://github.com/Scavenger233)
