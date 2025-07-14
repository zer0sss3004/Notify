import requests
from datetime import datetime, timezone
import yaml
from send_notify.constants import DEFAULT_TELEGRAM_CHATID

def send_to_msteams(webhook_url, card):
    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": card
            }
        ]
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, json=payload, headers=headers)
    return response.status_code, response.text

