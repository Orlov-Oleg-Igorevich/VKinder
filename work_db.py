import psycopg2
from  models import create_tables
import sqlalchemy
from sqlalchemy.orm import sessionmaker

import models as md

'''Коды ответа дял авторизации:
200 - клиент на стартовой страницы. Клавиатура - main
100 - клиент в режиме просмотра анкет. Клавиатура - session
101 - ожидание от клиента левой границы возраста. Клавиатура - search
102 - ожидание правой границы возраста. Клавиатура - search
103 - ожидание города. Клавиатура - search
104 - ожидание пола. Клавиатура - search_sex
105 - подтверждение поиска'''

#Создание самой Базы Данных
def create_data_base(name_postgres_base, user_postgres, password_postgres, name_DB):
    conn = psycopg2.connect(database=name_postgres_base,
        user=user_postgres, password=password_postgres)
    cur = conn.cursor()
    conn.autocommit = True
    sql = f"CREATE DATABASE {name_DB}"
    cur.execute(sql)
    print(f'Ваша база данных {name_DB} создана')
    cur.close()
    conn.close()

#create_data_base('postgres', 'postgres', '', 'VKinder')


def create_or_change_user(session, user_id, data):
    """Создание и изменение данных пользователя"""
    subq = session.query(md.ProgramUser).get(user_id)
    if subq is None:
        session.add(md.ProgramUser(user_id = user_id, name = data['first_name']))
    session.commit()

def checking_a_favorite(session, user_id):
    have = session.query(md.BridgeUserFavorites).filter(
        md.BridgeUserFavorites.program_user_id == user_id).first()
    if have:
        return True
    return None

def get_favorite(session, user_id):
    responses = session.query(md.ListOfFavorites).join(md.BridgeUserFavorites,
        md.BridgeUserFavorites.favorites_id == md.ListOfFavorites.favorites_id
    ).filter(md.BridgeUserFavorites.program_user_id == user_id).all()
    data = []
    for response in responses:
        data.append({
    'first_name': response.first_name,
    'last_name': response.last_name,
    'link_favorites': response.link_favorites,
    'photo1': response.photo1,
    'photo2': response.photo2,
    'photo3': response.photo3})
    return data




def add_favorite(session, user_id, favorites_id, data):
    """Добавление нового фаворита пользователю"""
    pk = session.query(md.ListOfFavorites).get(favorites_id)
    if pk:
        pk = pk.all()
        session.add(md.BridgeUserFavorites(favorites_id = favorites_id, program_user_id = user_id))
    else:
        session.add(md.ListOfFavorites(favorites_id = favorites_id, **data))
        session.commit()
        session.add(md.BridgeUserFavorites(program_user_id = user_id, favorites_id = favorites_id))
    session.commit()
    return True
