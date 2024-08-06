import psycopg2
import ast
from  models import create_tables
import sqlalchemy
from sqlalchemy.orm import sessionmaker


#Создание самой Базы Данных
# def create_data_base(name_postgres_base, user_postgres, password_postgres, name_DB):
#     conn = psycopg2.connect(database=name_postgres_base, user=user_postgres, password=password_postgres)
#     cur = conn.cursor()
#     conn.autocommit = True
#     sql = f"CREATE DATABASE {name_DB}"
#     cur.execute(sql)
#     print(f'Ваша база данных {name_DB} создана')
#     cur.close()
#     conn.close()
#create_data_base('postgres', 'postgres', '', 'VKinder')


DSN = 'postgresql://postgres:root@localhost:5432/vkinder'
engine = sqlalchemy.create_engine(DSN)
#Для создания таблиц базы данных
#create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()



session.close()

