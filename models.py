import sqlalchemy as alh
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# Таблицы Базы данных
class ProgramUser(Base):
    '''Модель пользователя'''
    __tablename__ = "program_user"

    user_id = alh.Column(alh.BIGINT, primary_key=True)
    name = alh.Column(alh.String(length=60))

    def __str__(self):
        return f'{self.name}'


class ListOfFavorites(Base):
    '''Модель человека, найденного при запросе пользователя. Далее -> фаворит'''
    __tablename__ = "favorites"

    favorites_id = alh.Column(alh.BIGINT, primary_key=True)
    first_name = alh.Column(alh.String(length=60))
    last_name = alh.Column(alh.String(length=60))
    link_favorites = alh.Column(alh.String(length=150))
    photo1 = alh.Column(alh.String(length=100))
    photo2 = alh.Column(alh.String(length=100))
    photo3 = alh.Column(alh.String(length=100))

    def __str__(self):
        return f'{self.name} {self.gender}.\
        Возраст: {self.age}. Город: {self.city}. Профиль: {self.link_favorites}'


class BridgeUserFavorites(Base):
    '''Модель для связи пользователей и фаворитов. Тип связи -> многие ко многим'''
    __tablename__ = "bridge_user_favorites"

    id = alh.Column(alh.Integer, primary_key=True)
    favorites_id = alh.Column(alh.Integer, ForeignKey('favorites.favorites_id'))
    program_user_id = alh.Column(alh.Integer,
        ForeignKey('program_user.user_id', ondelete='CASCADE'))

    def __str__(self):
        return f'{self.program_user_id} - {self.favorites_id}'


# Создание таблиц Баз данных
def create_tables(engine):
    '''Создание всех таблиц'''

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
