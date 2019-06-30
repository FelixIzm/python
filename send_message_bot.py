
import requests

def send_telegram(text: str):
    token = "bot829992269:AAHyL9GAswU2aGi7FzlRB9ORCEweVDU-hB4"
    url = "https://api.telegram.org/bot"
    channel_id = "486441898"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })

    if r.status_code != 200:
        raise Exception("post_text error")

if __name__ == '__main__':
  send_telegram("hello world!")