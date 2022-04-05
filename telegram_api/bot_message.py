from decouple import config
import requests

# telegram api
token_api = config('token_api', default='')
channel_id_api = config('channel_id_api', default='')
url_api = "https://api.telegram.org/bot"


def send_photo_telegram(files, text):
    token = token_api
    url = url_api
    channel_id = channel_id_api
    url += token
    method = url + "/sendPhoto"
    r = requests.post(method, data={
        "chat_id": channel_id, "caption": text,
    }, files=files)

    if r.status_code != 200:
        raise Exception("post_text error")


def send_text_telegram(text: str):
    token = token_api
    url = url_api
    channel_id = channel_id_api
    url += token
    method = url + "/sendMessage"
    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": text
    })
    if r.status_code != 200:
        raise Exception("post_text error")
