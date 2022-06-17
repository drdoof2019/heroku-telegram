
import requests


def send_text_to_telegram(caption):
    #print("Buradasın")
    url = 'https://api.telegram.org/bot5383482183:AAG-KsOztqqJ_6dMFoqL17BucHxU5JMnVrU/sendMessage'

    params = {
             'chat_id':'-1001730339476',
             'text':caption,
             'parse_mode': 'markdownv2',
             'disable_web_page_preview':True
    }

    r = requests.post(url,data=params)
