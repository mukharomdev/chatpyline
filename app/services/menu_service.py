from linebot.models import FlexSendMessage
from linebot.models import (
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackTemplateAction,
    QuickReply,
    QuickReplyButton,
    MessageAction
)
from linebot.exceptions import LineBotApiError
from app.models.menu import MenuItem
from app.templates import menu_template
from app.extensions import db



def send_menu_options(event,user_id, line_bot_api):
    categories = db.session.query(MenuItem.category).distinct().all()
    
    items = [
        QuickReplyButton(
            action=MessageAction(label=cat[0], text=f"Menu {cat[0]}")
        ) for cat in categories
    ]
    
    reply = TextSendMessage(
        text="Pilih kategori menu:",
        quick_reply=QuickReply(items=items)
    )

    categoriID = [category[0] for category in categories]
   
    
    menu = event.message.text
   
    match menu:
        case  'Menu minuman':
            return send_menu_by_category(categoriID[0],user_id,line_bot_api)
        case "Menu makanan":
            return send_menu_by_category(categoriID[1],user_id,line_bot_api)
        case _:
            return line_bot_api.push_message(user_id, reply)

def send_menu_by_category(category, user_id, line_bot_api):
    try :

        items = MenuItem.query.filter_by(
            category=category,
            is_available=True
        ).all()
        print(items)
        # Konversi items ke list of dictionaries
        items_data = [{
            'id': item.id,
            'name': item.name,
            'desc': item.description,
            'price': item.price,
            "image_url":item.image_url
            # tambahkan field lain yang diperlukan template
        } for item in items]
        
        flex_message = FlexSendMessage(
            alt_text=f"Menu {category}",
            contents=menu_template.generate(items_data)
        )
        
        line_bot_api.push_message(user_id, flex_message)
    except LineBotApiError as e:
        print(f"Error sending message: {e.error.message}")
        print(f"Details: {e.error.details}")
        # Kirim pesan error default ke user
        line_bot_api.push_message(user_id, TextSendMessage(text="Maaf, terjadi kesalahan menampilkan menu."))
    except Exception as e:
        print(f"Unexpected error: {str(e)}")