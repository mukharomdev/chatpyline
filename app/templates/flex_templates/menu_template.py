def generate(menu_items):
    return {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": item.image_url,
                    "size": "full",
                    "aspectRatio": "20:13"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": item.name, "weight": "bold", "size": "xl"},
                        {"type": "text", "text": item.desc, "wrap": True},
                        {"type": "text", "text": item.price, "weight": "bold", "size": "lg"}
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "Tambah ke Keranjang",
                                "data": f"action=add_to_cart&item_id={item.id}"
                            }
                        }
                    ]
                }
            } for item in menu_items
        ]
    }