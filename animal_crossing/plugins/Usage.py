from nonebot import on_command, CommandSession

COMMANDLIST = """
【目前支持中英文"/" "!" "#"作为命令识别符】
命令如下：
#查看房间
/show
#查看价格列表
/price
#开房
/open
#添加价格
/add
#删除价格
/del
#关闭 房间名
/close
#排队 房间名
/join
#等待人数
/len
#退出
/exit
"""


# 使用帮助
@on_command('help', aliases=('帮助', '命令', '查看帮助'), only_to_me=False)
async def usage(session: CommandSession):
    await session.send(COMMANDLIST, at_sender=True)
