from nonebot import on_command, CommandSession
from .Object import Room


@on_command('exit', aliases=('退出', '退出岛'), only_to_me=False)
async def exit(session: CommandSession):
    user = session.event['user_id']
    room = Room()
    room.getRoom()
    id = room.inMember(user)
    ididid = room.inQueue(user)
    if id:
        room.exitMem(user, id)
        await session.send('成功退出岛')
        if room.getQueueLen(id) > 0:
            users = room.queue[id]
            user = list(users.keys())[0]
            room.addMember(user, id)
            ididid = room.inQueue(user)
            room.exitQueue(user, ididid)
            print(ididid)
            bot = session.bot
            print(f"请进入岛\n岛密码为："
                               f"{room.room[id]['passwd']}"
                               f"\n请在工作完成后使用 /exit 命令退出岛")
            # await bot.send_msg(message_type="private",
            #                    user_id={user},
            #                    message=f"请进入岛\n岛密码为："
            #                    f"{room.room[id]['passwd']}"
            #                    f"\n请在工作完成后使用 /exit 命令退出岛")
    elif ididid:
        room.exitQueue(user, ididid)
        await session.send('成功退出队列')
    else:
        await session.send('当前不在任何岛和队列中')
