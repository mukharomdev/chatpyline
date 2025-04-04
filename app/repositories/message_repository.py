from app.models.message import Message
from app.extensions import db

class MessageRepository:
    @staticmethod
    def create(user_id, message_text, message_type):
        message = Message(
            user_id=user_id,
            message_text=message_text,
            message_type=message_type
        )
        db.session.add(message)
        db.session.commit()
        return message
    
    @staticmethod
    def get_user_messages(user_id, limit=10):
        return Message.query.filter_by(user_id=user_id).order_by(
            Message.timestamp.desc()
        ).limit(limit).all()