# aiohttp2pydantic
Library to wrap aiohttp2requests into Pydantic objects

Usage:

```python
class ContactMessageForm(BaseModel):
    sender_name: str
    sender_email: str
    message: str

async def save_message(message: ContactMessageForm):
   ...

@routes.post('/contactForm')
@aiohttp_to_pydantic(ContactMessageForm)
async def contact_form(request: PydanticAiohttpRequest):
    await save_message(request.data)
    return web.Response(status=200, body=b'Ok')


app = web.Application()
app.add_routes(routes)
```

The original `web.Request` object is into `request.request`
