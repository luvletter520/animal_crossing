import datetime


# 判断今天是否为周末
def is_sunday():
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
    sunday = now.weekday()
    if sunday == 6:
        return True
    else:
        return False
