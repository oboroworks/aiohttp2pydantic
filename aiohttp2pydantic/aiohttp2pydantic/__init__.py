from functools import wraps
from pydantic import BaseModel
from typing import Type
from aiohttp import web

class PydanticAiohttpRequest:
    def __init__(self, request: web.Request, data: BaseModel):
        self.request = request
        self.data = data

def aiohttp_to_pydantic(model: Type[BaseModel]):
    def decorator(handler):
        @wraps(handler)
        async def wrapper(request: web.Request):
            method = request.method
            if method == 'GET':
                data = dict(request.query)
            elif request.content_type == 'application/json':
                data = await request.json()
            elif request.content_type == 'application/x-www-form-urlencoded':
                data = await request.post()
            else:
                data = await request.read()  # fallback

            validated = model(**data)
            pyd_request = PydanticAiohttpRequest(request, validated)
            return await handler(pyd_request)

        return wrapper
    return decorator