import psycopg2
from  models import create_tables
import sqlalchemy
from sqlalchemy.orm import sessionmaker

import models

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


DSN = 'postgresql://postgres:root@localhost:5432/vkinder'
engine = sqlalchemy.create_engine(DSN)
#Для создания таблиц базы данных
#models.create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

def send_status_and_json():
    pass






session.close()
