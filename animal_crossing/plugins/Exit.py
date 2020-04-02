from nonebot import on_command, CommandSession
from .Object import Room
import config


@on_command('exit', aliases=('退出', '退出岛'), only_to_me=False)
async def exit(session: CommandSession):
    user = str(session.event['user_id'])
    room = Room()
    id = room.inMember(user)
    ididid = room.inQueue(user)
    if id:
        room.exitMem(user, id)
        await session.send('成功退出岛')
        if room.getQueueLen(id) > 0:
            users = room.queue[id]
            user = list(users.keys())[0]
            room.addMember(user, id, False)
            ididid = room.inQueue(user)
            room.exitQueue(user, ididid)
            bot = session.bot
            await bot.send_msg(message_type="private",
                               user_id=int(user),
                               message=f"岛【{id}】队列已经排到你，"
                               f"你需要在{config.QUEUE_TIME_OUT}分钟内输入 /准备 命令获取岛密码，"
                               f"{config.QUEUE_TIME_OUT}分钟内未输入准备命令将视为过号，过号须重新排队拿号")
    elif ididid:
        room.exitQueue(user, ididid)
        await session.send('成功退出队列')
    else:
        await session.send('当前不在任何岛和队列中')
