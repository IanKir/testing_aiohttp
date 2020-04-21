from aiohttp import web
from typing import Dict, List

from test_web_server import db
from test_web_server.db import document
from test_web_server.middlewares import handle_404
import aiohttp_jinja2


# todo: download docs
#  https://developers.google.com/drive/api/v3/manage-downloads#python

# todo: simple authorization with
#  https://aiohttp-security.readthedocs.io/en/latest/example.html


async def index(request):
    # todo: добавить рендер страницы greeting_page.html
    #  с которой можно перейти на страницу регистрации пользователя
    return web.Response(text='Hello {}'.format(request))


@aiohttp_jinja2.template('document_list.html')
async def get_document_list(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(document.select())
        records = await cursor.fetchall()
        documents = [dict(record) for record in records]
        return {'documents': documents}


@aiohttp_jinja2.template('document_detail.html')
async def get_document_detail(request):
    async with request.app['db'].acquire() as conn:
        document_id = request.match_info.get('document_id')
        try:
            document_id = int(document_id)
        except ValueError:
            return await handle_404(request)
        try:
            one_document = await db.get_document(
                conn=conn, document_id=document_id,
            )
        except db.RecordNotFound as exception:
            raise web.HTTPNotFound(text=str(exception))
        return {'document': one_document}


@aiohttp_jinja2.template('document_edit.html')
async def add_document(request):
    """Записывает данные в бд"""
    if request.method == 'POST':
        async with request.app['db'].acquire() as conn:
            request_data = await request.post()
            try:
                await db.add_document(conn=conn, data_to_write=request_data)
            except db.AddNewFileProblem as exception:
                raise web.HTTPNotFound(text=str(exception.message))
            location = request.app.router['get_document_list'].url_for()
            raise web.HTTPFound(location=location)
    return {'document': ''}


@aiohttp_jinja2.template('document_edit.html')
async def update_document(request):
    """Перезаписывает данные в бд"""
    if request.method == 'POST':
        async with request.app['db'].acquire() as conn:
            request_data = await request.post()
            try:
                await db.update_document(conn=conn, data_to_overwrite=request_data)
            except db.UpdateFileProblem as e:
                raise web.HTTPNotFound(text=str(e.message))
            location = request.app.router['get_document_list'].url_for()
            raise web.HTTPFound(location=location)
    elif request.method == 'GET':
        async with request.app['db'].acquire() as conn:
            document_id = request.match_info.get('document_id')
            try:
                document_id = int(document_id)
            except ValueError:
                return await handle_404(request)
            one_document = await db.get_document(conn=conn, document_id=document_id)
            return {'document': one_document}
