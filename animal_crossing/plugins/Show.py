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
    text = room.to_string(config.GROUP_ID, room_id, session.event['message_type'] == 'group')
    await session.send(f'{text}\n========================\n（现在使用 /订阅 命令，当有新房间创建时叮咚会自动私聊通知你。）')
