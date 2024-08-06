import json

main_keyboard = {
    "one_time": False,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "Поиск 👁‍🗨"
            },
            "color": "positive"
        }],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "О проекте"
            },
            "color": "secondary"
        }
        ]
    ]
}

session_keyboard = {
    "one_time": False,
    "buttons": [
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"1\"}",
                    "label": "Нравится ❤"
                },
                "color": "positive"
            },
            {
                "action": {
                "type": "text",
                "payload": "{\"button\": \"2\"}",
                "label": "Дальше"
                },
                "color": "primary"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"3\"}",
                    "label": "В чёрный список 🚫"
                },
                "color": "negative"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"4\"}",
                    "label": "В избранное 👀"
                },
                "color": "secondary"
            }
        ]
    ]
}

main_keyboard = json.dumps(main_keyboard, ensure_ascii=False).encode('utf-8')
#main_keyboard = str(main_keyboard.decode('utf-8'))
session_keyboard = json.dumps(session_keyboard, ensure_ascii=False).encode('utf-8')
