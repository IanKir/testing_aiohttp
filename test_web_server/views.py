from aiohttp import web
from typing import Dict, List

from . import db
from .db import user, document
import aiohttp_jinja2


# todo: https://developers.google.com/drive/api/v3/manage-downloads#python
# todo: добавить страницу редактирования документа

async def index(request):
    # todo: добавить рендер страницы greeting_page.html
    #  с которой можно перейти на страницу регистрации пользователя
    return web.Response(text='Hello {}'.format(request))


@aiohttp_jinja2.template('document_list.html')
async def get_document_list(request) -> Dict[str, List[dict]]:
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(document.select())
        records = await cursor.fetchall()
        documents = [dict(q) for q in records]
        return {'documents': documents}


@aiohttp_jinja2.template('document_detail.html')
async def get_document_detail(request) -> Dict[str, dict]:
    async with request.app['db'].acquire() as conn:
        document_id = request.match_info.get('document_id')
        try:
            one_document = await db.get_document(conn=conn, document_id=document_id)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))
        return {'document': one_document}


@aiohttp_jinja2.template('document_edit.html')
async def add_document(request) -> Dict[str, str]:
    """Записывает данные в бд"""
    if request.method == 'POST':
        async with request.app['db'].acquire() as conn:
            data = await request.post()
            try:
                await db.add_document(conn=conn, data=data)
            except db.AddNewFileProblem as e:
                raise web.HTTPNotFound(text=str(e.message))
            location = request.app.router['get_document_list'].url_for()
            raise web.HTTPFound(location=location)
    return {'document': ''}


@aiohttp_jinja2.template('document_edit.html')
async def update_document(request) -> Dict[str, str]:
    """Перезаписывает данные в бд"""
    if request.method == 'POST':
        async with request.app['db'].acquire() as conn:
            data = await request.post()
            print(data)
            try:
                await db.update_document(conn=conn, data=data)
            except db.UpdateFileProblem as e:
                raise web.HTTPNotFound(text=str(e.message))
            location = request.app.router['get_document_list'].url_for()
            raise web.HTTPFound(location=location)
    elif request.method == 'GET':
        async with request.app['db'].acquire() as conn:
            document_id = request.match_info.get('document_id')
            one_document = await db.get_document(conn=conn, document_id=document_id)
            return {'document': one_document}
