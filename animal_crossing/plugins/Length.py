from nonebot import on_command, CommandSession
from .Object import Room
import time
import config


@on_command('len', aliases=('length', '排队长度', '等待人数', '查看队列等待人数', '排队人数'), only_to_me=True)
async def len(session: CommandSession):
    user = session.event['user_id']
    room = Room()
    if await room.check_group_member(user) is None:
        return
    room_id = room.in_member(user)
    queue_id = room.in_queue(user)
    if room_id:
        await session.send(f"你已在岛【{room_id}】中，如需退出岛请使用 /退出 命令", at_sender=True)
    elif queue_id:
        length = room.get_wait_len(str(user))
        if length is not None:
            output = f"你正在岛【{queue_id}】的队列中" \
                f"\n前方排队人数为：{length}人" \
                f"\n当前在岛上的人为:"
            for key, item in room.member[queue_id].items():
                output += f"\n{item['nickname']}（{key}），进房时间：{int((time.time() - item['time']) / 60)}分钟"
        else:
            output = "当前不在队列中"
        await session.send(output, at_sender=True)
    else:
        output = "你不在任何队列中"
        await session.send(output, at_sender=True)


@on_command('member', aliases=('成员', '岛上成员', '查看成员'), only_to_me=True)
async def len(session: CommandSession):
    user = session.event['user_id']
    room = Room()
    output = f"当前在岛上的人为:"
    arg = session.current_arg_text.strip()
    room_id = None
    if arg.isdigit() and user in config.SUPERUSERS and arg in room.room.keys():
        room_id = arg
    else:
        for key, item in room.room.items():
            if user == item['user']:
                room_id = key
    if room_id and room_id in room.room.keys():
        for key, item in room.member[room_id].items():
            output += f"\n{item['nickname']}（{key}），进房时间：{int((time.time() - item['time']) / 60)}分钟"
        await session.send(output)
    else:
        await session.send('你没有正在开门的岛，请使用 /开门 命令，输入正确格式开启')
