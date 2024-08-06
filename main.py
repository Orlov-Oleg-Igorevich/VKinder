from random import randrange
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import keyboard
import config
from API_VK import VK


vk = vk_api.VkApi(token=config.TOKEN)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message, key):
    vk.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'keyboard': key,
        'random_id': randrange(10 ** 7)
        })

def write_form(user_id, message, key, group_id='207439336'):
    upload_url = vk.method('photos.getMessagesUploadServer', {
        'group_id': group_id
    })["upload_url"]
    req = requests.post(upload_url, params={'access_token': config.TOKEN}, files={'file': open('C:/Users/Oleg/Desktop/VKinder/BD_telegram_bot.png', 'rb')}).json()
    req.update({'access_token': config.TOKEN, 'v': '5.199'})
    req = requests.post(VK.API_base_url + 'photos.saveMessagesPhoto', params=req).json()
    vk.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'keyboard': key,
        'attachment': f'photo{req['response'][0]['owner_id']}_{req['response'][0]['id']}',
        'random_id': randrange(10 ** 7)
        })
    
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text
            vk_client = VK(config.TOKEN, event.user_id)

            if request == "Начать":
                write_msg(event.user_id,
                        f"Хай,{vk_client.users_info()['first_name']}",
                        keyboard.main_keyboard)
            elif request == "Поиск 👁‍🗨":
                write_form(event.user_id, "Пока((", keyboard.session_keyboard)
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...", keyboard.main_keyboard)
