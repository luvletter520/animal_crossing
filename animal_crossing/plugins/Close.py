from nonebot import on_command, CommandSession
from .Object import Room
import config


@on_command('close', aliases=('关闭', '关门'), only_to_me=False)
async def close(session: CommandSession):
    room = Room()
    user_id = session.event['user_id']
    if await room.check_group_member(user_id) is None:
        return
    arg = session.current_arg_text.strip()
    room_id = None
    if arg.isdigit() and user_id in config.SUPERUSERS and arg in room.room.keys():
        room_id = int(arg)
    else:
        for key, item in room.room.items():
            if user_id == item['user']:
                room_id = key
    if room_id:
        users = list(room.member[room_id].keys()) + list(room.queue[room_id].keys())
        room.close(room_id)
        await session.send('已成功关闭岛门')
        for user in users:
            await session.bot.send_msg(message_type="private",
                                       user_id=int(user),
                                       message=f"岛【{room_id}】已关闭，已自动退出。")
    else:
        await session.send('你没有正在开门的岛，请使用 /开门 命令，输入正确格式开启')
