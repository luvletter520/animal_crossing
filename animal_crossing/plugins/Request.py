from nonebot import on_request, RequestSession

@on_request('group')
async def _(session: RequestSession):
    await session.approve()