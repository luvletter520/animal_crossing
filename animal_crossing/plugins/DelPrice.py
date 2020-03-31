from nonebot import on_command, CommandSession
from .PriceList import Price
import nonebot
import config


@on_command('del', aliases=('删除价格', 'delete'), only_to_me=True)
async def delete(session: CommandSession):
    price = Price()
    priceList = price.getPriceList()
    user = str(session.event["user_id"])
    # group = str(session.event["group_id"])
    group = str(config.GROUP_ID)
    if user not in priceList[group].keys():
        await session.send('没有记录')
    else:
        price.delPrice(group, user)
        await session.send('删除成功')


@nonebot.scheduler.scheduled_job('cron', hour='8,12,22', timezone='Asia/Shanghai')
async def _():
    bot = nonebot.get_bot()
    price = Price()
    groupList = price.getGroupList()
    price.delAll()
    for group in groupList:
        await bot.send_group_msg(group_id=int(group), message="价格列表清理成功")
