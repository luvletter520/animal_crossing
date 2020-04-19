from nonebot import on_command, CommandSession
from .Object import Room
import config


@on_command('join', aliases=('进房', '排队', '参加'), only_to_me=True)
async def join(session: CommandSession):
    details = session.get('details', prompt='请输入你想要进入的岛ID')
    details = str(details)
    room = Room()
    user_id = str(session.event['user_id'])
    if await room.check_group_member(session.event['user_id']) is None:
        return
    queue_id = room.in_queue(user_id)
    if details not in room.room.keys():
        await session.send('该岛不存在')
    elif user_id in room.member[details].keys() and room.member[details][user_id]['ready'] is True:
        await session.send('你已在岛中，岛密码为：' + room.room[details]["passwd"])
    elif queue_id:
        await session.send('你已在队列中，请勿重复排队或排多个队伍')
    else:
        if room.get_user_number(details) < int(room.room[details]['length']):
            room.add_member(user_id, details, session.event["sender"]['nickname'])
            await session.send(f'成功进入岛\n'
                               f'岛密码为：{room.room[details]["passwd"]}\n'
                               f'请在出岛后使用 /退出 命令退出该岛\n'
                               f'大头菜房请勿跑多趟，每次排队仅能跑一趟！')
        else:
            room.add_queue(user_id, details, session.event["sender"]['nickname'])
            length = room.get_wait_len(user_id)
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
