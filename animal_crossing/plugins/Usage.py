from nonebot import on_command, CommandSession

COMMANDLIST = """
【目前支持中英文"/" "!" "#"作为命令识别符】
命令如下：
/show  #查看所有岛
/open  #开门
/join  #排队 + 岛ID
/close  #关闭 + 岛ID
/len  #查看队列等待人数
/exit  #退出岛

/price  #查看价格列表
/add  #添加价格
/del  #删除价格
"""


# 使用帮助
@on_command('help', aliases=('帮助', '命令', '查看帮助'), only_to_me=False)
async def usage(session: CommandSession):
    await session.send(COMMANDLIST, at_sender=True)
