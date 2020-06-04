from nonebot import on_command, CommandSession
from .Object import Room

room = Room()


@on_command('sub', aliases=('订阅', 'subscribe'), only_to_me=True)
async def marry(session: CommandSession):
    user = session.event['user_id']
    if room.add_subscribe(user):
        await session.send('订阅成功！当有新房间创建时叮咚会自动私聊通知你，如需取消订阅可以使用 /退订 命令。')
    else:
        await session.send('订阅失败！你已订阅')


@on_command('unsub', aliases=('退订', 'unsubscribe'), only_to_me=True)
async def divorce(session: CommandSession):
    user = session.event['user_id']
    if room.del_subscribe(user):
        await session.send('退订成功！')
    else:
        await session.send('退订失败！你未订阅')
    pass
