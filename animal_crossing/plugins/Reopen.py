from nonebot import on_command, CommandSession, scheduler, get_bot
from .Object import Room
import common
import config
import time
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
    details = session.get('details', prompt=CREATE_USAGE)
    formatDetails = await getDetails(details)
    if formatDetails:
        for key, item in room.room.items():
            if user == item['user']:
                room.reopen(key, formatDetails[0], formatDetails[1])
                await session.send(f"重开成功")
                for user_id in room.member[key].keys():
                    bot = session.bot
                    await bot.send_msg(message_type="private",
                                       user_id=int(user_id),
                                       message=f"岛【{key}】修改了密码，"
                                       f"新密码为：{formatDetails[0]}")

                surplus = room.room[key]['length'] - len(room.member[key].keys())
                if surplus > 0 and len(room.queue[key].keys()) > 0:
                    i = 0
                    for queue_id, queue in room.queue[key].items():
                        room.addMember(queue_id, key, queue['nickname'], False)
                        room.exitQueue(user, key)
                        bot = session.bot
                        await bot.send_msg(message_type="private",
                                           user_id=int(user),
                                           message=common.read_format(key))
                        i += 1
                        if surplus == i:
                            break
                return
            else:
                await session.send(f"你尚未开启过岛，请使用 /开岛 命令，并输入正确格式开启")
    else:
        await session.finish('格式错误，岛密码必须为5位字母或数字，最大登岛人数为1～8人')


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
async def getDetails(str):
    match = re.match(r'([0-9A-Z]{5})[|]{0,1}([1-8]{0,1})', str.upper())
    if match:
        return match.groups()
    return None
