import datetime
import os
import json
import config


# 判断今天是否为周末
def is_sunday():
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
    sunday = now.weekday()
    if sunday == 6:
        return True
    else:
        return False


def read_json(path, default):
    if os.path.exists(path) is False:
        return default
    fo = open(path)
    data = json.load(fo)
    fo.close()
    return data


def read_format(room):
    return f"岛【{room}】队列已经排到你，" \
        f"你需要在{config.QUEUE_TIME_OUT}分钟内输入 /准备 命令获取岛密码，" \
        f"{config.QUEUE_TIME_OUT}分钟内未输入准备命令将视为过号，过号须重新排队拿号"
