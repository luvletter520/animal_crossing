from nonebot import on_command, CommandSession
from .Object import Room
import config


@on_command('join', aliases=('进房', '排队', '参加'), only_to_me=True)
async def join(session: CommandSession):
    details = session.get('details', prompt='请输入你想要进入的岛ID')
    details = str(details)
    room = Room()
    user_id = str(session.event['user_id'])
    queue_id = room.inQueue(user_id)
    if details not in room.room.keys():
        await session.send('该岛不存在')
    elif user_id in room.member[details].keys():
        await session.send('你已在岛中，岛密码为：' + room.room[details]["passwd"])
    elif queue_id:
        await session.send('你已在队列中，请勿重复排队或排多个队伍')
    else:
        # Room capacity
        if room.getUserNumber(details) < int(room.room[details]['length']):
            room.addMember(user_id, details, session.event["sender"]['nickname'])
            await session.send(f'成功进入岛\n岛密码为：{room.room[details]["passwd"]}\n请在出岛后使用 /退出 命令退出该岛')
        else:
            room.addQueue(user_id, details, session.event["sender"]['nickname'])
            length = room.getWaitLen(user_id)
            await session.send(f"成功进入队列\n"
                               f"前方队列长度为：{length}人")


@join.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['details'] = stripped_arg
        return
    if not stripped_arg:
        session.pause('不能返回空值，请重新输入')
    session.state[session.current_key] = stripped_arg
