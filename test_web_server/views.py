from aiohttp import web
from .db import user
import aiohttp_jinja2


@aiohttp_jinja2.template('index.html')
async def index(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(user.select())
        records = await cursor.fetchall()
        users = [dict(q) for q in records]
        return {'users': users}
