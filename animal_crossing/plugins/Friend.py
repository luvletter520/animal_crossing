import nonebot
import config
import aiocqhttp

bot = nonebot.get_bot()


@bot.on_request('friend')
async def handle_request(event: aiocqhttp.Event):
    try:
        await bot.get_group_member_info(group_id=config.GROUP_ID, user_id=event['user_id'])
        await bot.set_friend_add_request(flag=event['flag'])
    except nonebot.CQHttpError as e:
        # print(e)
        pass


# @nonebot.scheduler.scheduled_job('cron', minute='30', timezone='Asia/Shanghai')
# async def _():
#     room = Room()
#     room.claerAll()