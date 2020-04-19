from nonebot import on_command, CommandSession
from .Object import Room
import config


@on_command('show', aliases=('查看当前岛', '查看岛', '查看'), only_to_me=False)
async def show(session: CommandSession):
    user_id = session.event['user_id']
    room = Room()
    if await room.check_group_member(user_id) is None:
        return
    arg = session.current_arg_text.strip()
    room_id = None
    if arg.isdigit():
        room_id = int(arg)
    await session.send(room.to_string(config.GROUP_ID, room_id))
