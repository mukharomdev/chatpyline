from linebot.models import FlexSendMessage
from models.menu import MenuItem
from templates.flex_messages import menu_template

def send_menu_options(user_id, line_bot_api):
    categories = db.session.query(MenuItem.category).distinct().all()
    
    items = [
        QuickReplyButton(
            action=MessageAction(label=cat[0], text=f"Menu {cat[0]}")
        ) for cat in categories
    ]
    
    reply = TextSendMessage(
        text="Pilih kategori menu:",
        quick_reply=QuickReply(items=items)
    
    line_bot_api.push_message(user_id, reply)
    

def send_menu_by_category(category, user_id, line_bot_api):
    items = MenuItem.query.filter_by(
        category=category,
        is_available=True
    ).all()
    
    flex_message = FlexSendMessage(
        alt_text=f"Menu {category}",
        contents=menu_template.generate(items)
    )
    
    line_bot_api.push_message(user_id, flex_message)