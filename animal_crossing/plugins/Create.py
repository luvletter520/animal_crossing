from nonebot import on_command, CommandSession, scheduler
from .Object import Room
import config
import re

CREATE_USAGE = """请将如下格式填写完整并发送
========================
格式：/开门 岛密码|价格|[最大登岛人数(可选，默认""" + str(config.DEFAULT_CAPACITY) + """人)]
示例1：/开门 GTX98|605
示例2：/开门 GTX98|605|4"""


@on_command('create', aliases=('open', '开房', '开门', '开启'), only_to_me=True)
async def create(session: CommandSession):
    room = Room()
    user_id = session.event['user_id']
    for key, item in room.room.items():
        if user_id == item['user']:
            await session.finish(f'你已有岛开启中，岛ID为：{key}，如需更新岛密码请使用 /重开 命令，如需关闭岛请使用 /关门 命令')
    details = session.get('details', prompt=CREATE_USAGE)
    TurnipDetails = await getTurnipDetails(details)
    formatDetails = await getDetails(details)
    if TurnipDetails is not None:
        room_id = 0
        if TurnipDetails[2]:
            room_id = room.open(TurnipDetails[0], None, TurnipDetails[1], config.GROUP_ID, session.event['user_id'],
                                session.event["sender"]['nickname'],
                                int(TurnipDetails[2]))
        else:
            room_id = room.open(TurnipDetails[0], None, TurnipDetails[1], config.GROUP_ID, session.event['user_id'],
                                session.event["sender"]['nickname'])
        await session.send(f'发布成功\n类型:大头菜\n岛ID为：{room_id}')
    elif formatDetails is not None:
        room_id = 0
        if formatDetails[2]:
            room_id = room.open(formatDetails[0], formatDetails[1], None, config.GROUP_ID, session.event['user_id'],
                                session.event["sender"]['nickname'],
                                int(formatDetails[2]))
        else:
            room_id = room.open(formatDetails[0], formatDetails[1], None, config.GROUP_ID, session.event['user_id'],
                                session.event["sender"]['nickname'])
        await session.send(f'发布成功\n岛ID为：{room_id}')
    if TurnipDetails is None and formatDetails is None:
        await session.finish('格式错误，岛密码必须为5位字母或数字，价格必须大于10并小于1000，最大登岛人数为1～7人')


@create.args_parser
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
    match = re.match(r'([0-9A-Za-z]{5})[|]([^|]{1,30})[|]{0,1}([1-7]{0,1})', str)
    if match:
        return match.groups()
    return None


async def getTurnipDetails(str):
    match = re.match(r'([0-9A-Za-z]{5})[|]([\d]{2,3})[|]{0,1}([1-7]{0,1})', str)
    if match:
        return match.groups()
    return None


@scheduler.scheduled_job('cron', hour='8,12,24', timezone='Asia/Shanghai')
async def _():
    room = Room()
    room.claerTurnipRoom()


@scheduler.scheduled_job('cron', hour='4', timezone='Asia/Shanghai')
async def _():
    room = Room()
    room.claerAll()


@scheduler.scheduled_job('interval', minutes=1)
async def _():
    room = Room()
    room.save()
