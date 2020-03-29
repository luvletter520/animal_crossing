from nonebot import on_command, CommandSession
from .Object import Room


@on_command('exit', aliases=('退出', '退出房间'), only_to_me=False)
async def exit(session: CommandSession):
    user = session.event['user_id']
    room = Room()
    room.getRoom()
    id = room.inMember(user)
    ididid = room.inQueue(user)
    if id:
        room.exitMem(user, id)
        await session.send('成功退出房间')
        if room.getQueueLen(id) > 0:
            user = room.queue[id][0]
            room.addMember(user, id)
            ididid = room.inQueue(user)
            room.exitQueue(user, ididid)
            print(ididid)
            bot = session.bot
            await bot.send_group_msg(group_id=session.event["group_id"],
                                     message=f"请[CQ:at,qq={user}]进入房间\n房间密码为：{room.room[id]['passwd']}\n请在工作完成后使用 /exit 命令退出房间")
            print(f"请[CQ:at,qq={user}]进入房间\n房间密码为：{room.room[id]['passwd']}\n请在工作完成后使用 /exit 命令退出房间")
    elif ididid:
        room.exitQueue(user, ididid)
        await session.send('成功退出队列')
    else:
        await session.send('当前不在任何房间和队列中')



