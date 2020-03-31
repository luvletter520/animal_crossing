from nonebot import on_command, CommandSession
from .Object import Room
import config

CREATE_USAGE = """请将如下表格填写完整并发送
========================
岛密码：
当前价格：
"""


@on_command('create', aliases=('open', '开房', '开门', '开启'), only_to_me=True)
async def create(session: CommandSession):
    details = session.get('details', prompt=CREATE_USAGE)
    try:
        formatDetails = await getDetails(details)
    except:
        session.finish('格式错误，重新输入')
    room = Room()
    id = room.open(formatDetails, config.GROUP_ID, session.event['user_id'], session.event["sender"]['nickname'])
    await session.send(f'发布成功\n岛ID为：{id}')


@create.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['details'] = stripped_arg
        return
    if not stripped_arg:
        session.pause('不能返回空值，请重新输入')
    session.state[session.current_key] = stripped_arg


# 表格内容解析
async def getDetails(str):
    str = str.replace('\r', '')
    firstStrList = str.split('\n')
    secStrList = []
    for string in firstStrList:
        secStrList.append(string.split('：')[1])
    secStrList[1] = int(secStrList[1])
    return secStrList
