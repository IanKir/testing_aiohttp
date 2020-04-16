import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, DateTime
)
from datetime import datetime

# todo: сделать хэшируемый пароль, не хранить его в открытом виде
#  есть функция hash, которая возвращает хэш от значения, которое ей передаешь
#  hash(request.POST.get('password')) во views.py
meta = MetaData()

user = Table(
    'user', meta,

    Column('id', Integer, primary_key=True),
    Column('username', String(200), nullable=False),
    Column('password_hash', String(100), nullable=False)
)

document = Table(
    'document', meta,

    Column('id', Integer, primary_key=True),
    Column('file_name', String(200), nullable=False),
    Column('publish_date', DateTime, nullable=False),
    Column('url', String(200), nullable=False),

    Column('user_id',
           Integer,
           ForeignKey('user.id', ondelete='CASCADE'))
)


async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
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
    app['db'].close()
    await app['db'].wait_closed()


class RecordNotFound(Exception):
    """Запрошенные данные в БД не найдены"""


class AddNewFileProblem(Exception):
    """Возникли проблемы при добавлении записи в БД"""

    def __init__(self, message):
        self.message = message


class UpdateFileProblem(Exception):
    """Возникли проблемы при добавлении записи в БД"""

    def __init__(self, message):
        self.message = message


async def get_document(conn, document_id):
    """Возвращает документ по его id"""
    result = await conn.execute(
        document.select().where(document.c.id == document_id))
    document_record = await result.first()
    if not document_record:
        msg = "Document with id: {} does not exists"
        raise RecordNotFound(msg.format(document_id))
    return document_record


async def add_document(conn, data):
    """Добавляет элемент в БД"""
    await conn.execute(
        document.insert().values(
            {'file_name': str(data.get('file_name')),
             'publish_date': datetime.now(),
             'url': str(data.get('url')),
             'user_id': int(data.get('user_id'))}))


async def update_document(conn, data):
    """Обновляет элемент в БД"""
    await conn.execute(
        document.update().where(
            document.c.id == int(data.get('document_id'))).values(
            {'file_name': str(data.get('file_name')),
             'publish_date': datetime.now(),
             'url': str(data.get('url')),
             'user_id': int(data.get('user_id'))}))
