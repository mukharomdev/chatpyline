from app import db

class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50))
    image_url = db.Column(db.String(255))
    is_available = db.Column(db.Boolean, default=True)
    
    def to_flex_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "desc": self.description,
            "price": f"Rp {self.price:,}",
            "image": self.image_url
        }