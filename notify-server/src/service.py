import requests


class TelegramMessage(object):
    def __init__(self, token: str, chat_ids: list) -> None:
        self.token = token
        self.chat_ids = chat_ids
        self.url = f"https://api.telegram.org/bot{token}/sendMessage"

    def send(self, message):
        status = []
        for chat_id in self.chat_ids:
            data = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML",
            }
            resp = requests.post(url=self.url, data=data)
            status.append(resp.text)
        return status
