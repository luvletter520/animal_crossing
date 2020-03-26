from nonebot import on_command, CommandSession
from .PriceList import Price


@on_command('del', aliases=('删除价格'), only_to_me=False)
async def delete(session: CommandSession):
    price = Price()
    priceList = price.getPriceList()
    if str(session.event["user_id"]) not in priceList.keys():
        await session.send('没有记录')
    else:
        priceList.delPrice(session.event["group_id"], session.event["user_id"])
        await session.send('删除成功')
