import nonebot
import config
import aiocqhttp
from .Object import Room

bot = nonebot.get_bot()


@bot.on_request('friend')
async def handle_request(event: aiocqhttp.Event):
    try:
        await bot.get_group_member_info(group_id=config.GROUP_ID, user_id=event.user_id)
        await bot.set_friend_add_request(flag=event.flag)
    except Exception as e:
        print(e)
        pass


@nonebot.scheduler.scheduled_job('interval', minutes=10)
async def _():
    member_list = await bot.get_group_member_list(group_id=config.GROUP_ID)
    members = {}
    for member in member_list:
        if len(member['card']) > 0:
            members[member['user_id']] = {
                'name': member['card']
            }
        else:
            members[member['user_id']] = {
                'name': member['nickname']
            }
    room = Room()
    room.group_member = members
    room.write('group_member')
