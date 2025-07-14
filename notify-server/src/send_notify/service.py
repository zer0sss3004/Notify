from datetime import datetime, timedelta

import pymsteams
import json
import requests
from send_notify.constants import DEFAULT_MSTEAM_WEBHOOK
from send_notify.schemas import TelegramMessage
from send_notify.utils import send_to_msteams
from utils import generate_response
from datetime import datetime, timedelta

time=datetime.now() +timedelta(hours=7)

def generate_message(title,field_values):
    lines = [f"⚠️ **{title}**", ""]
    for k, v in list(field_values.items())[1:]:
        lines.append(f"- **{k}**: {v}")
    return "\n".join(lines)

def generate_adaptive_card(title, field_values): #msteams card
    facts = [{"title": str(k), "value": str(v)} for k, v in field_values.items()]

    card = {
        "type": "AdaptiveCard",
        "version": "1.4",
        "body": [
            {
                "type": "TextBlock",
                "text": f"🔔 {title}",
                "weight": "Bolder",
                "size": "Large"
            },
            {
                "type": "FactSet",
                "facts": facts
            }
        ],
        "actions": [
            {
                "type": "Action.OpenUrl",
                "title": "✅ Xác nhận",
                "url": "https://your-confirm-url.com"
            },
            {
                "type": "Action.OpenUrl",
                "title": "🔍 Điều tra",
                "url": "https://your-investigation-url.com"
            },
            {
                "type": "Action.OpenUrl",
                "title": "❌ Bỏ qua",
                "url": "https://your-ignore-url.com"
            }
        ]
    }

    return card



def generate_interactive_message(title, field_values): #telegram
    message = f"<b>🔔 {title}</b>\n\n"
    for k, v in field_values.items():
        message += f"<b>{k}:</b> {v}\n"

    # Đây là phần inline keyboard
    inline_keyboard = {
        "inline_keyboard": [
            [
                {"text": "✅ Xác nhận", "callback_data": "confirm"},
                {"text": "🔍 Điều tra", "url": "https://your-investigation-url.com"}
            ],
            [
                {"text": "❌ Bỏ qua", "callback_data": "ignore"}
            ]
        ]
    }

    return message, inline_keyboard

def send_to_telegram(item,device_name):
    try:
        token = item.token

        #message, buttons = generate_interactive_message(item.title, item.field_values)
        message = generate_message(item.title, item.field_values)
        print(item.title)
        # print("Generated message:", message)


        data = {}
        data = item.field_values
        data["alert_name"] = item.title

        alert_query.save_alert('mycollection', data)
        # print("item title",item.title)

        filter_data = {'alert_name':item.title}
        print("filter",filter_data)

        now = datetime.now()
        fifteen_minutes_ago = now - timedelta(minutes=15)

        timestamp_now = int(now.timestamp())
        timestamp_15_min_ago = int(fifteen_minutes_ago.timestamp())

        print("now",timestamp_now)
        print("15m",timestamp_15_min_ago)

        # Count alerts
        count = alert_query.count_alerts('mycollection',filter_data,timestamp_15_min_ago,timestamp_now)
        print("count",count)


        chat_ids = item.chat_ids
        tele = TelegramMessage(token, chat_ids=chat_ids)
        if count < 5:
            result = tele.send(message)
            create_alert_vsmart(item,device_name)
        else:
            result = False
        # result = tele.send(message)
        # print("Send result:", result)

        if result is True:
            return generate_response(1, "/telegram/sendnotify", "Send information success", None)
        else:
            return generate_response(0, "/telegram/sendnotify", "Send failed: Telegram returned False", None)

    except Exception as e:
        print("Error sending to Telegram:", str(e))
        return generate_response(0, "/telegram/sendnotify", f"Send information fail: {str(e)}", None)

def send_case_to_telegram(item):
    try:
        token = item.token

        #message, buttons = generate_interactive_message(item.title, item.field_values)
        message = generate_message(item.title, item.field_values)

        print(item.field_values)
        # print("Generated message:", message)


        chat_ids = item.chat_ids
        tele = TelegramMessage(token, chat_ids=chat_ids)
        result = tele.send(message)

        # print("Send result:", result)

        if result is True:
            return generate_response(1, "/telegram/sendnotify", "Send information success", None)
        else:
            return generate_response(0, "/telegram/sendnotify", "Send failed: Telegram returned False", None)

    except Exception as e:
        print("Error sending to Telegram:", str(e))
        return generate_response(0, "/telegram/sendnotify", f"Send information fail: {str(e)}", None)

def send_to_teams(item, device_name):
    try:
        webhook_url = DEFAULT_MSTEAM_WEBHOOK  # Trong MS Teams, token = webhook URL
        message = generate_message(item.title, item.field_values)
        print(item.title)

        data = dict(item.field_values)  # clone dict để tránh thay đổi original
        data["alert_name"] = item.title

        # Tạo bộ lọc cho truy vấn
        filter_data = {'alert_name': item.title}
        print("filter", filter_data)

        now = datetime.now()
        fifteen_minutes_ago = now - timedelta(minutes=15)

        timestamp_now = int(now.timestamp())
        timestamp_15_min_ago = int(fifteen_minutes_ago.timestamp())

        # Gửi thông báo đến MS Teams
        payload = {
            "text": message
        }
        response = requests.post(webhook_url, json=payload)
        result = response.status_code == 200

        if result:
            return generate_response(1, "/msteam/sendnotify", "Send information success", None)
        else:
            return generate_response(0, "/msteam/sendnotify", "Send failed: MS Teams returned error", None)
    except Exception as e:
        print("Error sending to MS Teams:", str(e))
        return generate_response(0, "/msteam/sendnotify", f"Send information fail: {str(e)}", None)

def send_to_teams_card(item):
    try:
        webhook_url = item.webhook_url or DEFAULT_MSTEAM_WEBHOOK

        card = generate_adaptive_card(item.title, item.field_values)
        status_code, response_text = send_to_msteams(webhook_url, card)

        print("MS Teams status:", status_code)
        print("Response:", response_text)

        if status_code in [200, 201, 202]:
            return generate_response(1, "/teams/sendnotify", "Send to MS Teams success", None)
        else:
            return generate_response(0, "/teams/sendnotify", f"Send failed: {response_text}", None)

    except Exception as e:
        print("Error sending to MS Teams:", str(e))
        return generate_response(0, "/teams/sendnotify", f"Send information fail: {str(e)}", None)
