from pydantic import BaseModel
from typing import Union
import requests

class send_notify(BaseModel):

    title:Union[str,None]=None
    field_values: Union[dict,None]=None
    token: Union[str,None]=None
    chat_ids: Union[list,None]=None
    
class send_notify_msteam(BaseModel):

    title:Union[str,None]=None
    field_values: Union[dict,None]=None

class test(BaseModel):
    ip: Union[str, None] = None
class TelegramMessage:
    def __init__(self, token, chat_ids):
        self.token = token
        self.chat_ids = chat_ids

    def send(self, message, reply_markup=None):
        success = True
        for chat_id in self.chat_ids:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            if reply_markup:
                payload["reply_markup"] = reply_markup

            response = requests.post(url, json=payload)
            print(f"Send to {chat_id}: {response.status_code} - {response.text}")
            if response.status_code != 200:
                success = False
        return success
