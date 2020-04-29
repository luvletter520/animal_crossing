from nonebot import on_command, CommandSession, scheduler, get_bot
from .Object import Room
import config
import time


@on_command('ready', aliases=('准备',), only_to_me=True)
async def ready(session: CommandSession):
    user = str(session.event['user_id'])
    room = Room()
    if await room.check_group_member(session.event['user_id']) is None:
        return
    room_id = room.in_member(user)
    if room_id:
        member = room.member[room_id]
        now = time.time()
        if (now - member[user]['time']) > config.QUEUE_TIME_OUT * 60 and member[user]['ready'] is False:
            await session.send('准备失败，你已超过准备时间，请重新输入 /排队 命令排队拿号')
            room.exit_mem(user, room_id)
            await room.next_member(room_id)
        else:
            room_info = room.room[str(room_id)]
            # if room.member[room_id][user]['ready'] is False:
            #     await session.send(f'岛【{room_id}】有成员进入'
            #                        f'QQ号：{user}'
            #                        f'QQ昵称：{room.member[user]["nickname"]}')
            room.member[room_id][user]['ready'] = True
            await session.send(f'成功进入岛\n'
                               f'岛密码为：{room_info["passwd"]}\n'
                               f'请在出岛后使用 /退出 命令退出该岛\n'
                               f'大头菜房请勿跑多趟，每次排队仅能跑一趟！')
    else:
        room_id = room.in_queue(user)
        if room_id:
            await session.send(f'你已在岛【{room_id}】的队列中， 目前还没轮到你，请耐心等待')
        else:
            await session.send('准备失败，你可能未在队列中或超过准备时间，请排队拿号')


@scheduler.scheduled_job('interval', seconds=60)
async def _():
    room = Room()
    now = time.time()
    bot = get_bot()
    for room_id, member_list in room.member.items():
        for member_id, item in member_list.items():
            join_time = int((now - item['time']) / 60)
            if item['ready'] is False and join_time >= config.QUEUE_TIME_OUT:
                await bot.send_msg(message_type="private",
                                   user_id=int(member_id),
                                   message=f"你未准备, 你已超过准备时间, 请重新输入 /排队 命令排队拿号")
                room.exit_mem(member_id, room_id)
                await room.next_member(room_id)
            elif item['ready'] is True and (join_time - 10) >= 0 and (join_time - 10) % 5 == 0:
                if join_time > config.VIOLATION_TIME:
                    pass
                await bot.send_msg(message_type="private",
                                   user_id=int(member_id),
                                   message=f"你已经超过{join_time}分钟未退出房间，如已出岛请使用 /退出 命令退出房间。")
