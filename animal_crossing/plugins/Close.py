from nonebot import on_command, CommandSession
from .Object import Room
import config


@on_command('close', aliases=('关闭', '关门'), only_to_me=False)
async def close(session: CommandSession):
    room = Room()
    user_id = session.event['user_id']
    # is_admin = session.event['user_id'] not in config.SUPERUSERS
    room_id = None

    for key, item in room.room.items():
        if user_id == item['user']:
            room_id = key
    if room_id:
        room.close(room_id)
        await session.send('已成功关闭岛门')
    else:
        await session.send('你没有正在开门的岛，请使用 /开门 命令，输入正确格式开启')


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
