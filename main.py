from random import randrange, randint
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import keyboard
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import config
from API_VK import VK
import text_answer
import work_db
from datetime import date
import models


vk = vk_api.VkApi(token=config.TOKEN)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message, key):
    vk.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'keyboard': key,
        'random_id': randrange(10 ** 7)
        })

def write_form(user_id, message, key, links, group_id):
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
    req = requests.post(VK.API_base_url + 'photos.saveMessagesPhoto', params=req, timeout=10).json()
    list_ = []
    for value in req['response']:
        list_.append(f'photo{value['owner_id']}_{value['id']}')
    str_ = ','.join(list_)
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
    c = randint(1, 99)
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
    reqv = response['response']['items'][1]
    name, url_user  = reqv['text'].split('\n')
    first_name, last_name = name.split(' ')
    url_user = url_user.strip(' ').split(' ', maxsplit=1)[-1]
    data_ = {'first_name': first_name, 'last_name': last_name.strip('.'),
             'link_favorites': url_user}
    for i, photo_ in enumerate(reqv['attachments']):
        url = f'{photo_['photo']['owner_id']}_{photo_['photo']['id']}'
        data_[f'photo{i+1}'] = url
    return data_


if __name__ == "__main__":
    DSN = f'{config.DBMS}://{config.USER}:{config.PASSWORD}@{config.HOST}/{config.DB_NAME}'
    engine = sqlalchemy.create_engine(DSN)
    #Для создания таблиц базы данных
    #work_db.create_data_base(config.DBMS, config.USER, config.PASSWORD, config.DB_NAME)
    models.create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()


    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                vk_client = VK(config.TOKEN, event.user_id)
                name = vk_client.users_info('sex')['first_name']
                data = {'first_name': name}
                work_db.create_or_change_user(session, event.user_id, data)
                text_message = event.text
                if text_message == "Начать":
                    write_msg(event.user_id,
                            f"Привет, {name}",
                            keyboard.main_keyboard)

                elif text_message == "Поиск 👁‍🗨":
                    city = vk_client.users_info('city')['city']['id']
                    sex = vk_client.users_info('sex')['sex']
                    if sex == 2:
                        sex = 1
                    elif sex == 1:
                        sex = 2
                    par = {'city': city, 'sex': sex, 'count': 100, 'fields': ['domain'], 'offset': randint(1, 100)}
                    date_ = vk_client.users_info('bdate').get('bdate')
                    if date_ and date_.count('.') == 2:
                        age = int(str(date.today()).split('-', maxsplit=1)[0]) - \
                            int(vk_client.users_info('bdate')['bdate'].split('.')[2])
                        par.update({'age_from': age-1,'age_to': age+1})
                    data = get_a_favorite(par)
                    while work_db.checking_a_favorite(session, data['user_id']):
                        data = get_a_favorite(par)
                    vk_favorite = VK(config.access_token, data['user_id'])
                    resp = vk_favorite.get_all_photo()
                    ans = resp.get('response')
                    while not ans:
                        data = get_a_favorite(par)
                        vk_favorite = VK(config.access_token, data['user_id'])
                        resp = vk_favorite.get_all_photo()
                        ans = resp.get('response')
                    photo_album = []
                    for photo in ans['items']:
                        res = photo.get('orig_photo')
                        if res:
                            url = res['url']
                        else:
                            url = photo['sizes'][0]['url']
                        photo_album.append((photo['likes']['count'], url))
                    photo_album = sorted(photo_album, key=lambda x: x[0], reverse=True)
                    photo_album = [i[1] for i in photo_album]
                    write_form(event.user_id,
                            f'{data['first_name']} {data['last_name']}.\n\
                                Ссылка: {data['link']}',
                            keyboard.session_keyboard, photo_album[:3], longpoll.group_id)

                elif text_message == 'О проекте':
                    write_msg(event.user_id, text_answer.about, keyboard.main_keyboard)

                elif text_message == "Нравится ❤":
                    data = get_last_bot_message(event.user_id)
                    vk_favorite = VK(config.access_token, 1)
                    nick = data['link_favorites'].split('/')[-1]
                    favorite_id = vk_favorite.users_get(nick)['id']
                    work_db.add_favorite(session, event.user_id, favorite_id, data)

                elif text_message == "Дальше 👉":
                    city = vk_client.users_info('city')['city']['id']
                    sex = vk_client.users_info('sex')['sex']
                    if sex == 2:
                        sex = 1
                    elif sex == 1:
                        sex = 2
                    par = {'city': city, 'sex': sex, 'count': 100, 'fields': ['domain'], 'offset': randint(1, 100)}
                    date_ = vk_client.users_info('bdate').get('bdate')
                    if date_ and date_.count('.') == 2:
                        age = int(str(date.today()).split('-', maxsplit=1)[0]) - \
                            int(vk_client.users_info('bdate')['bdate'].split('.')[2])
                        par.update({'age_from': age-1,'age_to': age+1})
                    data = get_a_favorite(par)
                    while work_db.checking_a_favorite(session, data['user_id']):
                        data = get_a_favorite(par)

                    vk_favorite = VK(config.access_token, data['user_id'])
                    resp = vk_favorite.get_all_photo()
                    ans = resp.get('response')
                    while not ans:
                        data = get_a_favorite(par)
                        vk_favorite = VK(config.access_token, data['user_id'])
                        resp = vk_favorite.get_all_photo()
                        ans = resp.get('response')
                        print(1)
                    photo_album = []
                    for photo in ans['items']:
                        res = photo.get('orig_photo')
                        if res:
                            url = res['url']
                        else:
                            url = photo['sizes'][0]['url']
                        photo_album.append((photo['likes']['count'], url))
                    photo_album = sorted(photo_album, key=lambda x: x[0], reverse=True)
                    photo_album = [i[1] for i in photo_album]
                    write_form(event.user_id,
                            f'{data['first_name']} {data['last_name']}.\n\
                                Ссылка: {data['link']}',
                            keyboard.session_keyboard, photo_album[:3], longpoll.group_id)

                elif text_message == "В чёрный список 🚫":
                    pass

                elif text_message == "В избранное 👀":
                    data = work_db.get_favorite(session, event.user_id)
                    ans = []
                    for i in data:
                        ans.append(f'{i["first_name"]} {i["last_name"]}: {i["link_favorites"]}')
                    message = '\n'.join(ans)
                    write_msg(event.user_id, message, keyboard.session_keyboard)

                else:
                    write_msg(event.user_id, text_answer.not_found, keyboard.main_keyboard)
