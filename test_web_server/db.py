"""Модуль работы с БД."""

from aiopg import sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, DateTime,
)
from datetime import datetime

# todo: сделать хэшируемый пароль, не хранить его в открытом виде
#  есть функция hash, которая возвращает хэш от значения, которое ей передаешь
#  hash(request.POST.get('password')) во views.py
meta = MetaData()
string_length = 200

user = Table(
    'users',
    meta,
    Column('id', Integer, primary_key=True),
    Column('username', String(length=string_length), nullable=False),
    Column('password_hash', String(length=string_length), nullable=False),
)

permission = Table(
    'permissions',
    meta,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('permission_name', String(length=string_length), nullable=False),
)

document = Table(
    'documents',
    meta,
    Column('id', Integer, primary_key=True),
    Column('file_name', String(length=string_length), nullable=False),
    Column('publish_date', DateTime, nullable=False),
    Column('url', String(length=string_length), nullable=False),
    Column('user_id', Integer, ForeignKey('user.id', ondelete='CASCADE')),
)


async def init_pg(app):
    """Инициализирует БД.

    Parameters:
        app: obj приложения
    """
    conf = app['config']['postgres']
    engine = await sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine


async def close_pg(app):
    """Осторожно завершает работу с БД.

    Parameters:
        app: obj приложения
    """
    app['db'].close()
    await app['db'].wait_closed()


class RecordNotFound(Exception):
    """Запрошенные данные в БД не найдены."""


class AddNewFileProblem(Exception):
    """Возникли проблемы при добавлении записи в БД."""

    def __init__(self, message):
        """Инициализирует instance ошибки.

        Parameters:
            message: Сообщение об ошибке
        """
        self.message = message


class UpdateFileProblem(Exception):
    """Возникли проблемы при добавлении записи в БД."""

    def __init__(self, message):
        """Инициализирует instance ошибки.

        Parameters:
            message: Сообщение об ошибке
        """
        self.message = message


async def get_document(conn, document_id: int):
    """Возвращает документ obj по его id.

    Parameters:
        document_id (int): primary key документа в БД
        conn: the connection to data base

    Returns:
        document_record: запись в БД по заданному id
    """
    result_form_db = await conn.execute(
        document.select().where(document.c.id == document_id),
    )
    document_record = await result_form_db.first()
    if not document_record:
        msg = 'Document with id: {0} does not exists'
        raise RecordNotFound(msg.format(document_id))
    return document_record


async def add_document(conn, data_to_write):
    """Добавляет элемент в БД.

    Parameters:
        conn: the connection to data base
        data_to_write: data to write in data base
    """
    await conn.execute(
        document.insert().values(
            {
                'file_name': str(data_to_write.get('file_name')),
                'publish_date': datetime.now(),
                'url': str(data_to_write.get('url')),
                'user_id': int(data_to_write.get('user_id')),
            },
        ),
    )


async def update_document(conn, data_to_overwrite):
    """Обновляет элемент в БД.

    Parameters:
        conn: the connection to data base
        data_to_overwrite: data to write in data base
    """
    await conn.execute(
        document.update().where(
            document.c.id == int(data_to_overwrite.get('document_id')),
        ).values(
            {
                'file_name': str(data_to_overwrite.get('file_name')),
                'publish_date': datetime.now(),
                'url': str(data_to_overwrite.get('url')),
                'user_id': int(data_to_overwrite.get('user_id')),
            },
        ),
    )
