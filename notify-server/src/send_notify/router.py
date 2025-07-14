import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../..", "src"))
import yaml

from send_notify.schemas import send_notify, test, send_notify_msteam
from fastapi import APIRouter, HTTPException,Depends, Request

from utils import generate_response
from service import TelegramMessage
from send_notify.constants import DEFAULT_TELEGRAM_TOKEN ,DEFAULT_TELEGRAM_CHATID, DEFAULT_MSTEAM_WEBHOOK
from send_notify.service import generate_message, send_to_teams, send_to_teams_card

router = APIRouter()
@router.post("/telegram/sendnotify", tags=["Telegram"])
def splunk_send_to_telegram(item:send_notify):
    try:
        token = item.token
        
        message=generate_message(item.title,item.field_values)
        print(item)
        print(message)
        chat_ids = item.chat_ids
        tele = TelegramMessage(token, chat_ids=chat_ids)
        a=tele.send(message)
        print(a)
    except Exception as e:
        generate_response(0, "/telegram/sendnotify", "Send information fail", None)
    return generate_response(1, "/telegram/sendnotify", "Send information success", None)

@router.post("/msteam/sendnotify", tags=["MS Teams"])
def splunk_send_to_msteam(item:send_notify_msteam, request: Request):
    device_name = request.headers.get('X-Device-Name', 'Không rõ')
    return send_to_teams(item,device_name)


@router.post("/msteam/sendnotify_card", tags=["MS Teams"])
def splunk_send_card_to_msteam(item: send_notify_msteam):
    return send_to_teams_card(item)
