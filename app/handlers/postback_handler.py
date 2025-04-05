from linebot.models import PostbackEvent

def handle_postback(event, line_bot_api):
    data = event.postback.data
    user_id = event.source.user_id
    
    if data.startswith('action=add_to_cart'):
        from services.order_service import add_to_cart
        item_id = data.split('&')[1].split('=')[1]
        add_to_cart(user_id, item_id, line_bot_api)
    
    elif data == 'action=view_cart':
        from services.order_service import view_cart
        view_cart(user_id, line_bot_api)