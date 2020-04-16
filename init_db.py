from sqlalchemy import create_engine, MetaData

from test_web_server.settings import config
from test_web_server.db import user, document


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[user, document])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(user.insert(), [
        {'username': 'testuser',
         'password_hash': str(hash('testuser'))}
    ])
    conn.execute(document.insert(), [
        {'file_name': 'Полезные сайты для программирования',
         'publish_date': '2015-12-15 17:17:49.629+02',
         'url': 'https://docs.google.com/document/d/1x5U4xrnYm-dOa7LhBah7TKRs3IWU96ttY2m2r3n2Oq8/edit?usp=sharing',
         'user_id': 1},
        {'file_name': 'Онлайн ресурсы для изучения программирования',
         'publish_date': '2016-12-15 17:17:49.629+02',
         'url': 'https://docs.google.com/document/d/12vSuKV63-Xh9jT0rxA149weLXX-uXPJh4hRdh0mlq1I/edit?usp=sharing',
         'user_id': 1},
    ])
    conn.close()


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)
