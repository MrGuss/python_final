"""
В этом файле создаётся базовый класс SQLAlchemy для моделей, например Base = DeclarativeBase(). Этот файл является единым источником Base для всех ORM-моделей. Здесь не должно быть моделей пользователей и т.д., только базовая декларация.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
