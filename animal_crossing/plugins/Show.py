from nonebot import on_command, CommandSession
from .Object import Room
import nonebot
from aiocqhttp.exceptions import Error as CQHttpError


@on_command('show', aliases=('查看当前房间', '查看房间', '查看'), only_to_me=False)
async def show(session: CommandSession):
    room = Room()
    await session.send(room.toString(session.event['group_id']))



@nonebot.scheduler.scheduled_job('interval', minutes=30)
async def _():
    bot = nonebot.get_bot()
    room = Room()
    groupList = set(room.getGroupList())
    for groupId in groupList:
        try:
            await bot.send_group_msg(group_id=groupId, message=room.toString(groupId))
        except CQHttpError:
            pass
