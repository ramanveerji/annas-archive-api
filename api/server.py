from sanic import Sanic

from . import handlers

app = Sanic("api")

app.add_route(handlers.recents, "/recents", name="Recents")
app.add_route(handlers.search, "/search", name="Search")
app.add_route(handlers.download, "/download", name="Download")
