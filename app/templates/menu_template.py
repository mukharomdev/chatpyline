def generate(menu_items):
    print(menu_items)
    return {
        "type": "carousel",
        "contents": [
        {
       "type": "bubble",
        "hero": {
            "type": "image",
            "url": item['image_url'],
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {
                "type": "uri",
                "uri": "http://example.com"
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": item['name'],
                    "weight": "bold",
                    "size": "xl",
                    "wrap": True
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"Rp{item['price']}",
                            "weight": "bold",
                            "size": "md",
                            "flex": 0,
                            "color": "#009688"
                        }
                    ]
                },
                {
                    "type": "text",
                    "text": item['desc'],
                    "size": "sm",
                    "wrap": True,
                    "margin": "lg",
                    "color": "#666666"
                }
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
                        "label": "Pesan Sekarang",
                        "data": f"action=order&item={item['name']}"
                    },
                    "style": "primary",
                    "color": "#009688"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "uri",
                        "label": "Detail Produk",
                        "uri": "http://example.com/detail"
                    },
                    "margin": "sm"
                }
            ]
        }
    }for item in menu_items
]
}
    
    
    
    
