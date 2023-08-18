from asyncio import create_task, sleep
from dataclasses import dataclass
from time import time

from sanic.request import Request
from sanic.response import HTTPResponse

TIMEOUT = 30 * 60
ERROR_TIMEOUT = 1 * 60


@dataclass
class Cache:
    response: HTTPResponse
    cache_time: int = TIMEOUT
    expires_at: float = None

    def __post_init__(self):
        self.expires_at = time() + self.cache_time

    def expires_in(self) -> int:
        return int(self.expires_at - time())

    def is_expired(self) -> bool:
        return self.expires_in() <= 0


class Storage:
    data: dict[str, Cache] = {}

    def add_response(self,
                     key: str,
                     response: HTTPResponse,
                     cache_time: int = TIMEOUT):
        self.data[key] = Cache(response, cache_time)

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
        first_run = False
        while True:
            self.remove_expired_items()
            await sleep(1)


def cache(func):
    storage = Storage()
    first_run = True

    async def wrapper(request: Request, *args, **kwargs) -> HTTPResponse:
        nonlocal first_run
        if storage.exists(request.url):
            return storage.get_response(request.url)
        response = await func(request, *args, **kwargs)
        storage.add_response(
            request.url, response,
            (TIMEOUT if response.status < 400 else ERROR_TIMEOUT))
        if first_run:
            create_task(coro=storage.manager(),
                        name=f"cacheManager:{func.__name__}")
            first_run = False
        return storage.get_response(request.url)

    return wrapper
