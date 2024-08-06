import sqlalchemy as alh
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# Таблицы Базы данных
class Program_user(Base):
    __tablename__ = "program_user"

    id_user = alh.Column(alh.BIGINT, primary_key=True)
    name = alh.Column(alh.String(length=60))

    def __str__(self):
        return f'{self.name}'


class List_of_favorites(Base):
    __tablename__ = "favorites"

    id_favorites = alh.Column(alh.Integer, primary_key=True)
    name = alh.String(alh.String(length=100))
    gender = alh.Column(alh.String(length=15))
    age = alh.Column(alh.Integer())
    city = alh.Column(alh.String(length=35))
    link_favorites = alh.Column(alh.VARCHAR(length=150))

    def __str__(self):
        return f'{self.name} {self.gender} {self.age} {self.city} {self.link_favorites}'


class Favorites_photo(Base):
    __tablename__ = "favorites_photo"

    id_photo = alh.Column(alh.Integer, primary_key=True)
    title = alh.Column(alh.String(length=60))
    count_like = alh.Column(alh.Integer())
    link = alh.Column(alh.VARCHAR(length=150))
    id_favorites = alh.Column(alh.Integer, ForeignKey('favorites.id_favorites', ondelete='CASCADE'))

    def __str__(self):
        return f'{self.title} {self.count_like} {self.link}'


class Bridge_user_favorites(Base):
    __tablename__ = "bridge_user_favorites"

    id = alh.Column(alh.Integer, primary_key=True)
    id_favorites = alh.Column(alh.Integer, ForeignKey('favorites.id_favorites'))
    id_program_user = alh.Column(alh.Integer, ForeignKey('program_user.id_user', ondelete='CASCADE'))

    def __str__(self):
        return f'{self.id_program_user} {self.id_favorites}'


# Создание таблиц Баз данных
def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)