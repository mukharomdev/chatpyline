from app.models.user import User
from app.extensions import db

class UserRepository:
    @staticmethod
    def get_by_line_user_id(line_user_id):
        return User.query.filter_by(line_user_id=line_user_id).first()
    
    @staticmethod
    def create(line_user_id, display_name=None):
        user = User(line_user_id=line_user_id, display_name=display_name)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def update_display_name(line_user_id, display_name):
        user = User.query.filter_by(line_user_id=line_user_id).first()
        if user:
            user.display_name = display_name
            db.session.commit()
        return user