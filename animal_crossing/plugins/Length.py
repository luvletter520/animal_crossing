from nonebot import on_command, CommandSession
from .Object import Room


@on_command('len', aliases=('length', '排队长度', '等待人数', '查看队列等待人数', '排队人数'), only_to_me=True)
async def len(session: CommandSession):
    user = session.event['user_id']
    room = Room()
    roomID = room.inMember(user)
    queueID = room.inQueue(user)
    if roomID:
        await session.send(f"你已在岛【{roomID}】中，如需退出岛请使用 /退出 命令", at_sender=True)
    elif queueID:
        length = room.getWaitLen(str(user))
        if length is not None:
            output = f"你正在岛【{queueID}】的队列中" \
                f"\n前方排队人数为：{length}人" \
                f"\n当前在岛上的人为:"
            for key, item in room.member[queueID].items():
                output += f"\n{item['nickname']}（{key}）"
        else:
            output = "当前不在队列中"
        await session.send(output, at_sender=True)
    else:
        output = "你不在任何队列中"
        await session.send(output, at_sender=True)


@on_command('member', aliases=('岛上成员', '查看成员'), only_to_me=True)
async def len(session: CommandSession):
    user = session.event['user_id']
    room = Room()
    room_id = None
    output = f"当前在岛上的人为:"
    for key, item in room.room.items():
        if user == item['user']:
            room_id = key
    if room_id:
        for key, item in room.member[room_id].items():
            output += f"\n{item['nickname']}（{key}）"
        await session.send(output)
    else:
        await session.send('你没有正在开门的岛，请使用 /开门 命令，输入正确格式开启')
