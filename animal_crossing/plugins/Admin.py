from nonebot import on_command, CommandSession
import config
# import os
# import sys


@on_command('msg', aliases=('message', '发言'), only_to_me=False)
async def message(session: CommandSession):
    user_id = session.event['user_id']
    arg = session.current_arg_text.strip()
    if len(arg) > 0 and user_id in config.SUPERUSERS:
        await session.bot.send_msg(message_type="group", group_id=config.GROUP_ID, message=arg)


# @on_command('rebot', aliases=('重启',), only_to_me=False)
# async def message(session: CommandSession):
#     user_id = session.event['user_id']
#
#     if user_id in config.SUPERUSERS:
#         try:
#             sys.exit(0)
#         finally:
#             os.system(f'python {os.getcwd()}\\main.py')
