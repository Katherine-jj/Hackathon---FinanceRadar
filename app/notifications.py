import requests
import os

WEBHOOK_URL = os.getenv("ALERT_WEBHOOK")

def send_alert_webhook(payload: dict):
    if not WEBHOOK_URL:
        return
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        # логировать
        print("notify err", e)
