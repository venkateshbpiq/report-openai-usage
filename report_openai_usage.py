import os
import datetime
import requests
import json

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Date range: past 7 days
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=7)

def get_usage(start_date, end_date):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    params = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat()
    }
    response = requests.get("https://api.openai.com/v1/dashboard/billing/usage", headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    usage_dollars = round(data.get("total_usage", 0) / 100.0, 2)
    return usage_dollars

def post_to_slack(message):
    payload = {
        "text": message
    }
    response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})
    response.raise_for_status()

def main():
    usage = get_usage(start_date, end_date)
    message = (
        f"📊 *OpenAI API Usage Report*\n"
        f"From {start_date} to {end_date - datetime.timedelta(days=1)}:\n"
        f"💰 Total Usage: *${usage}*"
    )
    post_to_slack(message)

if __name__ == "__main__":
    main()
