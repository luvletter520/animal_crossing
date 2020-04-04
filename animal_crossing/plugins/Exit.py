from nonebot import on_command, CommandSession
from .Object import Room
import config


@on_command('exit', aliases=('退出', '退出岛'), only_to_me=True)
async def exit(session: CommandSession):
    user = str(session.event['user_id'])
    room = Room()
    id = room.inMember(user)
    ididid = room.inQueue(user)
    if id:
        room.exitMem(user, id)
        await session.send('成功退出岛')
        if room.getQueueLen(id) > 0:
            users = room.queue[id]
            user = list(users.keys())[0]
            room.addMember(user, id, room.queue[id][user]['nickname'], False)
            ididid = room.inQueue(user)
            room.exitQueue(user, ididid)
            bot = session.bot
            await bot.send_msg(message_type="private",
                               user_id=int(user),
                               message=f"岛【{id}】队列已经排到你，"
                               f"你需要在{config.QUEUE_TIME_OUT}分钟内输入 /准备 命令获取岛密码，"
                               f"{config.QUEUE_TIME_OUT}分钟内未输入准备命令将视为过号，过号须重新排队拿号")
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
            if room.getQueueLen(id) > 0:
                users = room.queue[id]
                user = list(users.keys())[0]
                room.addMember(user, id, room.queue[id][user]['nickname'], False)
                ididid = room.inQueue(user)
                room.exitQueue(user, ididid)
                bot = session.bot
                await bot.send_msg(message_type="private",
                                   user_id=int(user),
                                   message=f"岛【{id}】队列已经排到你，"
                                   f"你需要在{config.QUEUE_TIME_OUT}分钟内输入 /准备 命令获取岛密码，"
                                   f"{config.QUEUE_TIME_OUT}分钟内未输入准备命令将视为过号，过号须重新排队拿号")
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
