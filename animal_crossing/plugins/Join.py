from nonebot import on_command, CommandSession
from .Object import Room
import config


@on_command('join', aliases=('进房', '排队', '参加'), only_to_me=False)
async def join(session: CommandSession):
    details = session.get('details', prompt='请输入你想要进入的房间ID')
    details = str(details)
    room = Room()
    room.getRoom()
    room.getMember()
    room.getQueue()
    if details not in room.room.keys():
        await session.send('房间不存在')
    elif session.event['user_id'] in room.member[details]["member"]:
        await session.send('您已在房间中')
    elif str(session.event['user_id']) in room.queue[details].keys():
        await session.send('您已在队列中')
    else:
        # Room capacity
        if room.getUserNumber(details) < config.CAPACITY:
            print(room.getUserNumber(details))
            room.addQueue(session.event['user_id'], details)
            room.addMember(session.event['user_id'], details)
            await session.send(f'成功进入房间\n房间密码为：{room.room[details]["passwd"]}\n请在工作完成后使用 /exit 命令退出房间')
        else:
            room.addQueue(session.event['user_id'], details)
            await session.send(f"成功进入队列\n队列序号为：{room.queue[details][str(session.event['user_id'])]}\n"
                               f"前方队列长度为：{room.getWaitLen(str(session.event['user_id']))}")



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
