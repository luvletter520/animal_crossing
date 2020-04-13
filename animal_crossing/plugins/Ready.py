from nonebot import on_command, CommandSession, scheduler, get_bot
from .Object import Room
import config
import time
import common


@on_command('ready', aliases=('准备',), only_to_me=True)
async def ready(session: CommandSession):
    user = str(session.event['user_id'])
    room = Room()
    id = room.inMember(user)
    if id:
        member = room.member[id]
        now = time.time()
        if (now - member[user]['time']) > config.QUEUE_TIME_OUT * 60:
            await session.send('准备失败，你已超过准备时间，请重新输入 /排队 命令排队拿号')
        else:
            room.member[id][user]['ready'] = True
            await session.send(f"请进入岛\n岛密码为："
                               f"{room.room[str(id)]['passwd']}"
                               f"\n请在出岛后使用 /退出 命令退出岛")
    else:
        await session.send('准备失败，你可能未在队列中或超过准备时间，请排队拿号')
    pass


@scheduler.scheduled_job('interval', minutes=1)
async def _():
    room = Room()
    now = time.time()
    bot = get_bot()
    for id, memList in room.member.items():
        for key, item in memList.items():
            join_time = int((now - item['time']) / 60)
            if item['ready'] is False and join_time > config.QUEUE_TIME_OUT:
                room.exitMem(key, id)
                await bot.send_msg(message_type="private",
                                   user_id=int(key),
                                   message=f"你未准备, 你已超过准备时间, 请重新输入 /排队 命令排队拿号")
                queue_ids = list(room.queue[id].keys())
                if len(queue_ids) > 0 and room.getUserNumber(id) < int(room.room[id]['length']):
                    user = queue_ids[0]
                    room.addMember(user, id, room.queue[id][user]['nickname'], False)
                    room.exitQueue(user, id)
                    await bot.send_msg(message_type="private",
                                       user_id=int(user),
                                       message=common.read_format(id))
            elif item['ready'] is True and (join_time - 10) > 0 and (join_time - 10) % 5 == 0:
                if join_time > config.VIOLATION_TIME:
                    pass
                await bot.send_msg(message_type="private",
                                   user_id=int(key),
                                   message=f"你已经超过{join_time}分钟未退出房间，如已出岛请使用 /退出 命令退出房间。")
