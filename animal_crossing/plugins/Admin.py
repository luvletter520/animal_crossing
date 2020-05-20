from nonebot import on_command, CommandSession, scheduler, get_bot
import config
import re
import common
import json
import aiocqhttp
from .Object import Room

bot = get_bot()


@on_command('msg', aliases=('message', '发言'), only_to_me=True)
async def message(session: CommandSession):
    user_id = session.event['user_id']
    arg = session.current_arg_text.strip()
    if len(arg) > 0 and user_id in config.SUPERUSERS:
        await session.bot.send_msg(message_type="group", group_id=config.GROUP_ID, message=arg)


@on_command('gag', aliases=('禁言',), only_to_me=True)
async def gag(session: CommandSession):
    user_id = session.event['user_id']
    arg = session.current_arg_text.strip()
    match = re.match(r'^([0-9]{6,15})[|]([0-9]{1,6})[|]?([^|]*)$', arg)
    if match and user_id in config.SUPERUSERS:
        groups = match.groups()
        await session.bot.set_group_ban(group_id=config.GROUP_ID, user_id=int(groups[0]), duration=int(groups[1]) * 60)
        if len(groups[2]) > 0:
            await session.bot.send_msg(message_type="group",
                                       group_id=config.GROUP_ID,
                                       message=f'“{groups[2]}”\nQQ号：[CQ:at,qq={groups[0]}] 被管理员 叮咚 禁言{groups[1]}分钟')
        else:
            await session.bot.send_msg(message_type="group",
                                       group_id=config.GROUP_ID,
                                       message=f'QQ号：[CQ:at,qq={groups[0]}] 被管理员 叮咚 禁言{groups[1]}分钟')
        await session.send('禁言成功！')


@on_command('rebot', aliases=('重启',), only_to_me=False)
async def message(session: CommandSession):
    user_id = session.event['user_id']

    if user_id in config.SUPERUSERS:
        info = common.read_json('animal_crossing/data/pid.json', False)
        if info is not False:
            fo = open('animal_crossing/data/pid.json', "w")
            info['rebot'] = True
            fo.write(json.dumps(info))
            fo.flush()
            fo.close()


@bot.on_message('private')
async def handle_msg(event: aiocqhttp.Event):
    user_id = str(event.user_id)
    message_text = str(event.message)
    room = Room()
    if message_text.find('/msg') != -1 or event.user_id == 1702955399:
        return
    member = room.group_member.get(str(user_id), -1)
    if member != -1:
        nickname = member['name']
    else:
        nickname = event.sender["nickname"]
    await bot.send_msg(message_type="private",
                       user_id=1702955399,
                       message=f'{nickname}({event.user_id}): {message_text}')


@on_command('p', aliases=('私聊',), only_to_me=True)
async def gag(session: CommandSession):
    user_id = session.event['user_id']
    arg = session.current_arg_text.strip()
    match = re.match(r'^([0-9]{6,15})[|]([\s\S]{1,300})$', arg)
    if match and user_id in config.SUPERUSERS:
        groups = match.groups()
        receiver = int(groups[0])
        message_text = groups[1]
        tip = '发送成功！'
        await session.bot.send_msg(message_type="private",
                                   user_id=receiver,
                                   message=message_text)
        await session.send(tip)
