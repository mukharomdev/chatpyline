from app.extensions import db

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message_text = db.Column(db.Text)
    message_type = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    
    def __repr__(self):
        return f'<Message {self.id}>'