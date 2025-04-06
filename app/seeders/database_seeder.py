from app import create_app, db
from app.models.menu import MenuItem
from app.seeders.seed_data import menu_data, user_data
import random
from datetime import datetime, timedelta

def seed_menus():
    """Seed product data"""
    print("Seeding menus...")
    for data in menu_data:
        menu = MenuItem(
            name=data['name'],
            description=data.get('desc', ''),
            price=data['price'],
            category=data['category'],
            image_url=data['image']
        )
        db.session.add(menu)
    db.session.commit()

def seed_users():
    """Seed user data"""
    print("Seeding users...")
    for data in user_data:
        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],  # Note: Store hashed passwords in production
            is_admin=data.get('is_admin', False)
        )
        db.session.add(user)
    db.session.commit()


def run_seeders():
    app = create_app()
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # Run seeders
        # seed_users()
        seed_menus()
       
        
        print("Database seeding completed successfully!")

if __name__ == '__main__':
    run_seeders()