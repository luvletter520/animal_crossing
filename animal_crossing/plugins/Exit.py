from nonebot import on_command, CommandSession
from .Object import Room
import config
import common


@on_command('exit', aliases=('退出', '退出岛'), only_to_me=True)
async def exit(session: CommandSession):
    user = str(session.event['user_id'])
    room = Room()
    id = room.inMember(user)
    ididid = room.inQueue(user)
    if id:
        room.exitMem(user, id)
        await session.send('成功退出岛')
        if room.getQueueLen(id) > 0 and room.getUserNumber(id) < int(room.room[id]['length']):
            users = room.queue[id]
            user = list(users.keys())[0]
            room.addMember(user, id, room.queue[id][user]['nickname'], False)
            room.exitQueue(user, id)
            await session.bot.send_msg(message_type="private",
                                       user_id=int(user),
                                       message=common.read_format(id))
    elif ididid:
        room.exitQueue(user, ididid)
        await session.send('成功退出队列')
    else:
        await session.send('当前不在任何岛和队列中')


@on_command('kick', aliases=('踢人',), only_to_me=True)
async def kick(session: CommandSession):
    details = session.get('details', prompt='请输入你要踢的人QQ号')
    room = Room()
    room_id = None
    users = []
    if details == '全部' or details.upper() == 'ALL':
        user_id = session.event['user_id']
        for key, item in room.room.items():
            if user_id == item['user']:
                room_id = key
                break
    if room_id:
        users = list(room.member[room_id].keys())
    else:
        users = [str(details)]
    for user in users:
        id = room.inMember(user)
        if id:
            if room.room[id]['user'] != session.event['user_id']:
                await session.finish("未找到对应QQ号人员")
            room.exitMem(user, id)
            await session.send(f'成功将{user}踢出岛')
            await session.bot.send_msg(message_type="private",
                                       user_id=int(user),
                                       message=f"你已被岛【{id}】的岛主移除出岛")
            if room.getQueueLen(id) > 0 and room.getUserNumber(id) < int(room.room[id]['length']):
                users = room.queue[id]
                user = list(users.keys())[0]
                room.addMember(user, id, room.queue[id][user]['nickname'], False)
                room.exitQueue(user, id)
                bot = session.bot
                await bot.send_msg(message_type="private",
                                   user_id=int(user),
                                   message=common.read_format(id))
        else:
            await session.finish("未找到对应QQ号人员")


@kick.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['details'] = stripped_arg
        return
    if not stripped_arg:
        session.pause('不能返回空值，请重新输入')
    session.state[session.current_key] = stripped_arg
