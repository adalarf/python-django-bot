from asgiref.sync import async_to_sync


@async_to_sync
async def make_async_to_sync(func):
    return await func
