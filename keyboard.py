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
                "payload": "{\"button\": \"2\"}",
                "label": "О проекте"
            },
            "color": "secondary"
        }],
        [{
            'action': {
                'type': 'text',
                'payload': "{\"button\": \"3\"}",
                'label': '"В избранное 👀"'
            }
        }]
    ]
}

search_keyboard = {
    'one_time': False,
    'buttons': [
        [{
            'action': {
                'type': 'text',
                'payload': "{\"button\": \"1\"}",
                'label': 'Не имеет значения'
            },
            'color': 'secondary'
        }]
    ]
}

search_sex_keyboard = {
    'one_time': False,
    'buttons': [
        [
            {
                'action': {
                    'type': 'text',
                    'payload': "{\"button\": \"1\"}",
                    'label': 'муж'
                },
                'color': 'primary'
            },
            {
                'action': {
                    'type': 'text',
                    'payload': "{\"button\": \"2\"}",
                    'label': 'жен'
                },
                'color': 'primary'
            }
        ],
        [{
            'action': {
                'type': 'text',
                'payload': "{\"button\": \"3\"}",
                'label': 'Не имеет значения'
            },
            'color': 'secondary'
        }]
    ]
}

approval_keyboard = {
    'one_time': False,
    'buttons': [
        [{
            'action': {
                'type': 'text',
                'payload': "{\"button\": \"1\"}",
                'label': 'Выполнить поиск'
            },
            'color': 'primary'
        },
        {
            'action': {
                'type': 'text',
                'patload': "{\"button\": \"2\"}",
                'label': 'Заполнить запрос заного'
            },
            'color': 'secondary'
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
                "label": "Дальше =>"
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
search_keyboard = json.dumps(search_keyboard, ensure_ascii=False).encode('utf-8')
search_sex_keyboard = json.dumps(search_sex_keyboard, ensure_ascii=False).encode('utf-8')
approval_keyboard = json.dumps(approval_keyboard, ensure_ascii=False).encode('utf-8')
