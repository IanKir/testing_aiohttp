import aiohttp_jinja2
import jinja2
from aiohttp import web

from test_web_server.db import init_pg, close_pg
from test_web_server.settings import config, BASE_DIR
from test_web_server.routes import setup_routes

app = web.Application()
setup_routes(app)
app['config'] = config
aiohttp_jinja2.setup(app,
                     loader=jinja2.FileSystemLoader(str(BASE_DIR / 'test_web_server' / 'templates')))
app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)
web.run_app(app)
