from flask import Blueprint, request, jsonify
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from app.config import Config
from app.services.line_bot_service import LineBotService
from app.repositories.user_repository import UserRepository
from app.repositories.message_repository import MessageRepository
from app.nlp import handle_message_nlp
webhook_bp = Blueprint('webhook', __name__)

handler = WebhookHandler(Config.lineChannelSecret)

@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return jsonify({"status": "error", "message": "Invalid signature"}), 400
    
    return jsonify({"status": "success"}), 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    message_text = event.message.text
    
    # Get or create user
    user = UserRepository.get_by_line_user_id(user_id)
    if not user:
        profile = LineBotService.get_user_profile(user_id)
        display_name = profile.display_name if profile else None
        user = UserRepository.create(user_id, display_name)
    
    # Save message to database
    MessageRepository.create(user.id, message_text, 'text')
    
    # Process message and reply
    # response = f"Anda mengirim: {message_text}"
    # LineBotService.reply_message(event.reply_token, response)
    handle_message_nlp(event)