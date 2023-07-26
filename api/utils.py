from asyncio import create_task, sleep
from dataclasses import dataclass
from http import HTTPStatus
from time import time

from aiohttp import request
from sanic.request import Request
from sanic.response import HTTPResponse

CACHE_TIMEOUT = 30 * 60
ERROR_CACHED_TIMEOUT = 1 * 60


@dataclass(slots=True)
class Cache:
    response: HTTPResponse
    expires_at: float

    def expires_in(self) -> float:
        return self.expires_at - time()

    def is_expired(self) -> bool:
        return self.expires_in() <= 0


@dataclass(slots=True)
class Response:
    status_code: int
    text: str


async def http_get(url: str, params: dict = {}) -> Response:
    async with request("GET", url, params=params) as response:
        text = await response.text()
        return Response(response.status, text)


def cache(func):
    cache_storage: dict[str, Cache] = {}

    def remove_expired_items():
        for key, cache in cache_storage.items():
            if cache.is_expired():
                cache_storage.pop(key)

    async def clean_cache():
        while cache_storage:
            try:
                remove_expired_items()
            except:
                pass
            await sleep(1)

    async def wrapper(request: Request, *args, **kwargs) -> HTTPResponse:
        if not request.url in cache_storage:
            response = await func(request, *args, **kwargs)
            expires_at = time()
            if response.status >= HTTPStatus.INTERNAL_SERVER_ERROR:
                expires_at += ERROR_CACHED_TIMEOUT
            else:
                expires_at += CACHE_TIMEOUT
            cache_storage[request.url] = Cache(response, expires_at)
            if len(cache_storage) == 1:
                create_task(coro=clean_cache(), name=f"cacheCleaner:{func.__name__}")
        cache = cache_storage[request.url]
        cache.response.headers["Cache-Control"] = f"max-age={cache.expires_in()}"
        return cache.response

    return wrapper
