from nonebot import on_command, CommandSession
from .Object import Room
import config


@on_command('close', aliases=('关闭',), only_to_me=False)
async def close(session: CommandSession):
    details = session.get('details', prompt='请输入你想要关闭的岛ID')
    details = str(details)
    room = Room()
    if details not in room.room.keys():
        await session.send('该岛不存在')
    elif session.event['user_id'] not in [room.room[details]["user"], list(config.SUPERUSERS)[0]]:
        await session.send('你没有关闭权限')
    else:
        room.close(details)
        await session.send('已成功关闭岛门')


@close.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['details'] = stripped_arg
        return
    if not stripped_arg:
        session.pause('不能返回空值，请重新输入')
    session.state[session.current_key] = stripped_arg
