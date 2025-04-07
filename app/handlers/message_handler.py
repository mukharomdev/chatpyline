from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    QuickReply, QuickReplyButton, MessageAction
)

def handle_text_message(event, line_bot_api):
    user_message = event.message.text.lower()
    
    if 'menu' in user_message:
        from app.services.menu_service import send_menu_options
        send_menu_options(event.source.user_id, line_bot_api)
        
    elif 'pesan' in user_message or 'order' in user_message:
        from app.services.order_service import start_order_flow
        start_order_flow(event.source.user_id, line_bot_api)
    elif 'promo' in user_message:
        from app.services.promo_service import send_current_promos
        send_current_promos(event.source.user_id, line_bot_api)
    else:
        reply = TextSendMessage(
            text="Halo! Silakan pilih opsi:\n1. Lihat Menu\n2. Buat Pesanan\n3. Cek Promo",
            quick_reply=QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="Menu", text="Menu")),
                QuickReplyButton(action=MessageAction(label="Pesan", text="Pesan")),
                QuickReplyButton(action=MessageAction(label="Promo", text="Promo"))
            ])
        )
        line_bot_api.reply_message(event.reply_token, reply)