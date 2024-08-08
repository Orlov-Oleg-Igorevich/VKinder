from random import randrange
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import keyboard
import config
from API_VK import VK
import text_answer
import work_db


vk = vk_api.VkApi(token=config.TOKEN)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message, key):
    vk.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'keyboard': key,
        'random_id': randrange(10 ** 7)
        })

def write_form(user_id, message, key, links, group_id='207439336'):
    upload_url = vk.method('photos.getMessagesUploadServer', {
        'group_id': group_id
    })["upload_url"]
    count = 0
    for num, link in enumerate(links):
        content = requests.get(link, timeout=10).content
        with open(f'photo{num}.jpg', 'wb') as f:
            f.write(content)
            count += 1
    if count == 1:
        req = requests.post(upload_url, params={'access_token': config.TOKEN},
            files={'file1': open('photo0.jpg', 'rb')},
                timeout=10).json()
    elif count == 2:
        req = requests.post(upload_url, params={'access_token': config.TOKEN},
            files={'file1': open('photo0.jpg', 'rb'), 'file2': open('photo1.jpg', 'rb')},
                timeout=10).json()
    else:
        req = requests.post(upload_url, params={'access_token': config.TOKEN},
            files={'file1': open('photo0.jpg', 'rb'), 'file2': open('photo1.jpg', 'rb'), 'file3': open('photo2.jpg', 'rb')},
                timeout=10).json()
    req.update({'access_token': config.TOKEN, 'v': '5.199'})
    print(req)
    req = requests.post(VK.API_base_url + 'photos.saveMessagesPhoto', params=req, timeout=10).json()
    list_ = []
    for value in req['response']:
        list_.append(f'photo{value['owner_id']}_{value['id']}')
    str_ = ','.join(list_)
    print(len(req['response']))
    vk.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'keyboard': key,
        'attachment': str_,
        'random_id': randrange(10 ** 7)
        })

def get_a_favorite(params):
    url = VK.API_base_url + 'users.search'
    params_base = {'access_token': config.access_token, 'v': '5.199'}
    params_base.update(params)
    response = requests.get(url, params=params_base, timeout=10).json()
    c = 40
    user_id = response['response']['items'][c]['id']
    first_name = response['response']['items'][c]['first_name']
    last_name = response['response']['items'][c]['last_name']
    link = 'https://vk.com/' + response['response']['items'][c]['domain']
    data = {'user_id': user_id, 'first_name': first_name, 'last_name': last_name, 'link': link}
    return data


def get_last_bot_message(peer_id):
    url = VK.API_base_url + 'messages.getHistory'
    params_base = {'access_token': config.TOKEN, 'v': '5.199', 'peer_id': peer_id}
    response = requests.get(url, params=params_base, timeout=10).json()
    return response['response']['items'][0]['text']

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            #response = work_db.user_authentication(event.user_id)
            text_message = event.text
            vk_client = VK(config.access_token, event.user_id)
            '''if response > 100:
                if response == 101:
                    try:
                        age_left = int(text_message)
                        if age_left < 10 or age_left > 99:
                            write_msg(event.user_id, 'Проверьте, пожалуйста, " \
                                      "корректность данных и введите двухзначное число',
                                      keyboard.search_keyboard)
                        else:
                            work_db.send_status_and_json(event.user_id, 102, text_message)
                            write_msg(event.user_id, 'Введите правую границу возраста для поиска',
                                    keyboard.search_keyboard)
                    except ValueError:
                        write_msg(event.user_id, 'Проверьте, пожалуйста, " \
                                      "корректность данных и введите двухзначное число',
                                      keyboard.search_keyboard)
                elif response == 102:
                    try:
                        age_right = int(text_message)
                        if age_right < 10 or age_left > 99:
                            write_msg(event.user_id, 'Проверьте, пожалуйста, " \
                                      "корректность данных и введите двухзначное число',
                                      keyboard.search_keyboard)
                        else:
                            work_db.send_status_and_json(event.user_id, 103, text_message)
                            write_msg(event.user_id, 'Введите город поиска',
                                    keyboard.search_keyboard)
                    except ValueError:
                        write_msg(event.user_id, 'Проверьте, пожалуйста, " \
                                      "корректность данных и введите двухзначное число',
                                      keyboard.search_keyboard)
                elif response == 103:
                    work_db.send_status_and_json(event.user_id, 104, text_message)
                    write_msg(event.user_id, 'Введите пол человека', keyboard.search_sex_keyboard)
                elif response == 104:
                    work_db.send_status_and_json(event.user_id, 105, text_message)
                    write_msg(event.user_id, 'Проверьте корректность данных',
                            keyboard.approval_keyboard)
                else:
                    if text_message == 'Заполнить запрос заного':
                        work_db.send_status_and_json(event.user_id, 101, None)
                        write_msg(event.user_id, 'Введите левую границу возраста для поиска',
                                keyboard.search_keyboard)
                    elif text_message == 'Выполнить поиск':
                        work_db.send_status(event.user_id, 100)
                        write_form(event.user_id, 'Введите левую границу возраста для поиска',
                                keyboard.session_keyboard)
                    else:
                        write_msg(event.user_id, 'Не удалось распознать команду.\n"\
                                "Пожалуйста, выберите из предложенных вариантов',
                                keyboard.approval_keyboard)'''

            if text_message == "Начать":
                write_msg(event.user_id,
                        f"Привет, {vk_client.users_info()['first_name']}",
                        keyboard.main_keyboard)
            elif text_message == "Поиск 👁‍🗨":
                work_db.get_status(event.user_id, 101)
                write_form(event.user_id, 'Введите левую границу возраста для поиска',
                        keyboard.session_keyboard)
            elif text_message == 'О проекте':
                print(get_last_bot_message(event.peer_id))
                write_msg(event.user_id, text_answer.about, keyboard.main_keyboard)
            elif text_message == "Нравится ❤":
                pass
            elif text_message == "Дальше":
                par = {'hometown':  'Москва', 'sex': 2, 'age_from': 17, 'age_to': 20, 'count': 50, 'fields': ['domain']}
                data = get_a_favorite(par)
                vk_favorite = VK(config.access_token, data['user_id'])
                photo_album = []
                for photo in vk_favorite.get_all_photo():
                    photo_album.append((photo['likes']['count'], photo['orig_photo']['url']))
                photo_album = sorted(photo_album, key=lambda x: x[0], reverse=True)
                photo_album = [i[1] for i in photo_album]
                write_form(event.user_id,
                        f'{data['first_name']} {data['last_name']}.', keyboard.main_keyboard, photo_album)
            elif text_message == "В чёрный список 🚫":
                pass
            elif text_message == "В избранное 👀":
                pass
            else:
                print(isinstance(get_last_bot_message(event.peer_id), int))
                write_msg(event.user_id, text_answer.not_found, keyboard.main_keyboard)
