from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
from config import Config

line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)

class LineBotService:
    @staticmethod
    def reply_message(reply_token, message):
        try:
            line_bot_api.reply_message(
                reply_token,
                TextSendMessage(text=message)
            )
        except LineBotApiError as e:
            print(f"Error when replying message: {e}")
    
    @staticmethod
    def get_user_profile(user_id):
        try:
            profile = line_bot_api.get_profile(user_id)
            return profile
        except LineBotApiError as e:
            print(f"Error getting user profile: {e}")
            return None