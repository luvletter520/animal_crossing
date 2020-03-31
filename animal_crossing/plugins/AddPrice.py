from nonebot import on_command, CommandSession
from .PriceList import Price
import config
import common


@on_command('add', aliases=('添加价格'), only_to_me=True)
async def add(session: CommandSession):
    details = session.get('details', prompt='请输入您的大头菜价格')
    try:
        details = int(details)
    except:
        session.finish('格式错误，重新输入')
    if (details > 110 or details < 90) and common.is_sunday():
        session.finish('白菜头价格错误')
    elif details < 0:
        session.finish('白菜头价格不能小于0')
    priceList = Price()
    priceList.addPrice(config.GROUP_ID, session.event["user_id"], session.event["sender"]['nickname'], details)
    await session.send('添加成功')


@add.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['details'] = stripped_arg
        return
    if not stripped_arg:
        session.pause('不能返回空值，请重新输入')
    session.state[session.current_key] = stripped_arg
