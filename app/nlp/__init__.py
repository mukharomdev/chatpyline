from linebot import LineBotApi, WebhookHandler
from linebot.models import TextMessage, MessageEvent, TextSendMessage
import requests
from config import *

line_bot_api = LineBotApi(lineChannelAccessToken)
def handle_message(event):
    user_message = event.message.text
    user_id = event.source.user_id

    # Kirim pesan ke Wit.ai untuk diproses
    wit_response = call_witai(user_message)
    intent = wit_response.get('intents', [{}])[0].get('name', 'unknown')
    confidence = wit_response.get('intents', [{}])[0].get('confidence', 0)

    # Logika respons berdasarkan intent
    if intent == 'greeting' and confidence > 0.8:
        reply_text = "Halo! Ada yang bisa saya bantu?"
    elif intent == 'ask_weather' and confidence > 0.7:
        reply_text = "Cuaca hari ini cerah!"
    else:
        reply_text = "Maaf, saya tidak mengerti."

    # Balas ke pengguna LINE
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

# Panggil Wit.ai API
def call_witai(text):
    headers = {
        'Authorization': f'Bearer {nlpClientToken}',
        'Content-Type': 'application/json'
    }
    params = {'q': text}
    response = requests.get(nlpClientUrl, headers=headers, params=params)
    return response.json()



__ALL__ = [handle_message]