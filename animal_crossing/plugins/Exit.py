from nonebot import on_command, CommandSession
from .Object import Room


@on_command('exit', aliases=('退出', '退出房间'), only_to_me=False)
async def exit(session: CommandSession):
    user = session.event['user_id']
    room = Room()
    room.getRoom()
    id = room.inMember(user)
    pos = room.getQueueNum(user)
    if id:
        room.exitMem(user, id)
        await session.send('成功退出房间')
        pos += 1
        for mem, num in room.queue[id].items():
            if pos == num:
                room.addMember(mem, id)
                bot = session.bot
                await bot.send_group_msg(group_id=session.event["group_id"], message=f"请[CQ:at,qq={mem}]进入房间\n房间密码为：{room.room[id]['passwd']}\n请在工作完成后使用 /exit 命令退出房间")
