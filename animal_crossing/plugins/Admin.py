from nonebot import on_command, CommandSession, scheduler, get_bot
import config
import re
import common
import json


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
    match = re.match(r'^([0-9]{6,15})[|]([0-9]{1,6})$', arg)
    if match and user_id in config.SUPERUSERS:
        groups = match.groups()
        await session.bot.set_group_ban(group_id=config.GROUP_ID, user_id=int(groups[0]), duration=int(groups[1]) * 60)
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
