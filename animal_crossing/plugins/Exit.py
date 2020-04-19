from nonebot import on_command, CommandSession
from .Object import Room
import config
import common


@on_command('exit', aliases=('退出', '退出岛'), only_to_me=True)
async def exit_room(session: CommandSession):
    room = Room()
    user_id = session.event['user_id']
    if await room.check_group_member(user_id) is None:
        return
    user_id = str(user_id)
    room_id = room.in_member(user_id)
    queue_id = room.in_queue(user_id)
    if room_id:
        room.exit_mem(user_id, room_id)
        await session.send('成功退出岛')
        await room.next_member(room_id)
    elif queue_id:
        room.exit_queue(user_id, queue_id)
        await session.send('成功退出队列')
    else:
        await session.send('当前不在任何岛和队列中')


@on_command('kick', aliases=('踢人',), only_to_me=True)
async def kick(session: CommandSession):
    details = session.get('details', prompt='请输入你要踢的人QQ号')
    room = Room()
    user_id = session.event['user_id']
    if await room.check_group_member(user_id) is None:
        return
    room_id = None
    if details == '全部' or details.upper() == 'ALL':
        for key, item in room.room.items():
            if user_id == item['user']:
                room_id = key
                break
    if room_id:
        users = list(room.member[room_id].keys())
    else:
        users = [str(details)]
    for user in users:
        room_id = room.in_member(user)
        if room_id:
            if room.room[room_id]['user'] != session.event['user_id']:
                await session.finish("未找到对应QQ号人员")
            room.exit_mem(user, room_id)
            await session.send(f'成功将{user}踢出岛')
            await session.bot.send_msg(message_type="private",
                                       user_id=int(user),
                                       message=f"你已被岛【{room_id}】的岛主移除出岛")
            await room.next_member(room_id)
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
