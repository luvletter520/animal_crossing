from nonebot import on_command, CommandSession
import random


@on_command('roll', aliases=('r', '随机', '巨魔', 'troll'), only_to_me=False)
async def message(session: CommandSession):
    user_id = session.event['user_id']
    arg = session.current_arg_text.strip()
    strs = arg.split('|')
    remark = None
    if len(strs) >= 2:
        remark = strs[1]
        arg = strs[0]
    range_number = 6
    if arg.isdigit():
        arg = int(arg)
    else:
        arg = 6
    number = 0
    if arg <= 6:
        number = random.randint(1, 6)
    elif arg <= 12:
        range_number = 12
        number = random.randint(1, 12)
    elif arg <= 100 or arg > 100:
        range_number = 100
        number = random.randint(1, 100)
    if remark:
        await session.send(f'{remark}\n[CQ:at,qq={user_id}]\n你随机的点数为：{number}\n随机范围为：1 - {range_number}')
    else:
        await session.send(f'[CQ:at,qq={user_id}]\n你随机的点数为：{number}\n随机范围为：1 - {range_number}')
