import os
from datetime import datetime, timedelta
import time
import requests
from airtable import Airtable

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE = "Tasks"
AIRTABLE_KEY = os.getenv("AIRTABLE_API_KEY")
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")

airtable = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE, AIRTABLE_KEY)

def parse_task(text):
    return {"Task": text, "Time": (datetime.utcnow() + timedelta(minutes=1)).isoformat(), "Status": "Open"}

def send_slack(msg):
    requests.post(SLACK_WEBHOOK, json={"text": msg})

def main_loop():
    send_slack("✅ Slack assistant is now live.")
    while True:
        records = airtable.get_all(formula="Status='Open'")
        for r in records:
            fields = r['fields']
            task_time = datetime.fromisoformat(fields['Time'])
            if task_time <= datetime.utcnow():
                send_slack(f"⏰ Reminder: {fields['Task']}")
                airtable.update(r['id'], {"Status": "Done"})
        time.sleep(30)

if __name__ == "__main__":
    main_loop()
