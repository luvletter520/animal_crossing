from nonebot import on_command, CommandSession, scheduler, get_bot
from .Object import Room
import common
import re


CREATE_USAGE = """请将如下格式填写完整并发送
========================
格式[岛密码]|[最大登岛人数(可选，默认不修改人数)]
示例：GTX98
示例2：GTX98|5
"""


@on_command('reopen', aliases=('重开', '更新岛密码'), only_to_me=True)
async def reopen(session: CommandSession):
    user = session.event['user_id']
    room = Room()
    user_id = session.event['user_id']
    if await room.check_group_member(user_id) is None:
        return
    details = session.get('details', prompt=CREATE_USAGE)
    format_details = await get_details(details)
    is_reopen = False
    if format_details:
        for room_id, item in room.room.items():
            if user == item['user']:
                room.reopen(room_id, format_details[0], format_details[1])
                await session.send(f"重开成功")
                for user_id in room.member[room_id].keys():
                    bot = session.bot
                    await bot.send_msg(message_type="private",
                                       user_id=int(user_id),
                                       message=f"岛【{room_id}】修改了密码，"
                                       f"新密码为：{format_details[0]}")
                member_count = len(room.member[room_id].keys())
                surplus = room.room[room_id]['length'] - member_count
                bot = session.bot
                if surplus > 0 and len(room.queue[room_id].keys()) > 0:
                    i = 0
                    for queue_id, queue in room.queue[room_id].items():
                        if i < member_count:
                            if surplus == i:
                                await bot.send_msg(message_type="private",
                                                   user_id=int(queue_id),
                                                   message=f"岛【{room_id}】的排队下一位就轮到你了，请提前做好准备")
                            else:
                                await bot.send_msg(message_type="private",
                                                   user_id=int(queue_id),
                                                   message=f"岛【{room_id}】修改了密码，可能队伍等待时间会变长，请耐心等待")
                        await room.add_member(queue_id, room_id, queue['nickname'], False)
                        room.exit_queue(queue_id, room_id)
                        await bot.send_msg(message_type="private",
                                           user_id=int(queue_id),
                                           message=common.read_format(room_id))
                        i += 1

                is_reopen = True
        if is_reopen is False:
            await session.send(f"你尚未开启过岛，请使用 /开岛 命令，并输入正确格式开启")
    else:
        await session.finish('格式错误，岛密码必须为5位字母或数字，最大登岛人数为1～7人')


@reopen.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['details'] = stripped_arg
        return
    if not stripped_arg:
        session.pause('不能输入空值，请重新输入')
    session.state[session.current_key] = stripped_arg


# 表格内容解析
async def get_details(details):
    match = re.match(r'^([0-9A-Z]{5})[|]{0,1}([1-8]{0,1})$', details.upper())
    if match:
        return match.groups()
    return None
