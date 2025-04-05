from linebot.models import (
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackTemplateAction,
    QuickReply,
    QuickReplyButton,
    MessageAction
)

def handle_message(event, line_bot_api):
    user_message = event.message.text.lower()
    user_id = event.source.user_id
    
    if "menu" in user_message:
        show_menu(event, line_bot_api)
    elif "pesan" in user_message or "order" in user_message:
        ask_order_details(event, line_bot_api)
    elif "help" in user_message:
        send_help_message(event, line_bot_api)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Halo! Mau pesan apa hari ini? 🍔")
        )

def show_menu(event, line_bot_api):
    # Contoh: Mengambil data menu dari database
    from models.menu import Menu
    menus = Menu.query.limit(5).all()
    
    menu_list = "\n".join([f"{m.name} - Rp {m.price}" for m in menus])
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text=f"📋 Menu Hari Ini:\n{menu_list}\n\nKetik 'pesan [nama menu]' untuk memesan.",
            quick_reply=QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="Lihat Menu", text="menu")),
                QuickReplyButton(action=MessageAction(label="Pesan", text="pesan"))
            ])
        )
    )

def ask_order_details(event, line_bot_api):
    buttons = ButtonsTemplate(
        title="Konfirmasi Pesanan",
        text="Pilih metode pembayaran:",
        actions=[
            PostbackTemplateAction(label="Tunai", data="payment_method=cash"),
            PostbackTemplateAction(label="OVO/GOPAY", data="payment_method=ewallet")
        ]
    )
    
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(alt_text="Pilih pembayaran", template=buttons)
    )

def handle_postback(event, line_bot_api):
    data = event.postback.data
    
    if data.startswith("payment_method="):
        payment_method = data.split("=")[1]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"Pesanan diterima! Pembayaran via {payment_method}. Terima kasih! 🎐")
        )