from nonebot import on_command, CommandSession
from .Object import Room

@on_command('len', aliases=('length', '排队长度', '等待人数'), only_to_me=False)
async def len(session: CommandSession):
    user = session.event['user_id']
    room = Room()
    room.getQueue()
    if room.inMember(user):
        await session.send(f"\n您已在房间【{room.inMember(user)}】", at_sender=True)
    else:
        output = f"\n您前方排队人数为：{room.getWaitLen(session.event['user_id'])}" if room.getWaitLen(session.event['user_id']) else "当前不在队列中"
        await session.send(output, at_sender=True)