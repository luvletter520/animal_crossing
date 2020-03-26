from nonebot import on_command, CommandSession
from .PriceList import Price
import nonebot

@on_command('del', aliases=('删除价格'), only_to_me=False)
async def delete(session: CommandSession):
    price = Price()
    priceList = price.getPriceList()
    if str(session.event["user_id"]) not in priceList.keys():
        await session.send('没有记录')
    else:
        priceList.delPrice(session.event["group_id"], session.event["user_id"])
        await session.send('删除成功')

@nonebot.scheduler.scheduled_job('cron', hour='0,12', timezone='Asia/Shanghai')
async def _():
    bot = nonebot.get_bot()
    price = Price()
    groupList = price.getGroupList()
    price.delAll()
    for group in groupList:
        await bot.send_group_msg(group_id=int(group), message="价格列表清理成功")