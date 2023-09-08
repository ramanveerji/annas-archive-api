from asyncio import create_task, sleep
from dataclasses import dataclass
from time import time

from sanic.request import Request
from sanic.response import HTTPResponse

DEFAULT_TIMEOUT = 30 * 60
ERROR_TIMEOUT = 1 * 60


@dataclass(slots=True)
class Cache:
    response: HTTPResponse
    cache_time: int = DEFAULT_TIMEOUT
    expires_at: float = None

    def __post_init__(self):
        self.expires_at = time() + self.cache_time

    def expires_in(self) -> int:
        return int(self.expires_at - time())

    def is_expired(self) -> bool:
        return self.expires_in() <= 0


class Storage:
    data: dict[str, Cache] = {}
    manager_running = False

    def __init__(self, name: str):
        self.name = name

    async def add_response(self, key: str, response: HTTPResponse, cache_time: int):
        self.data[key] = Cache(response, cache_time)
        if not self.manager_running:
            create_task(coro=self.manager(), name=f"cacheManager:{self.name}")

    def get_response(self, key: str) -> Cache:
        c = self.data[key]
        c.response.headers["Cache-Control"] = f"max-age={c.expires_in()}"
        return c.response

    def exists(self, key: str) -> bool:
        return key in self.data

    def remove_expired_items(self):
        expireds = list(filter(lambda i: i[1].is_expired(), self.data.items()))
        for key, _ in expireds:
            self.data.pop(key)

    async def manager(self):
        self.manager_running = True
        while True:
            self.remove_expired_items()
            await sleep(1)


def cache(func):
    storage = Storage(func.__name__)

    async def wrapper(request: Request, *args, **kwargs) -> HTTPResponse:
        url = request.url
        if storage.exists(url):
            return storage.get_response(url)
        response = await func(request, *args, **kwargs)
        timeout = DEFAULT_TIMEOUT if response.status < 400 else ERROR_TIMEOUT
        await storage.add_response(url, response, timeout)
        return storage.get_response(url)

    return wrapper
