import psutil
import os
import time
import common

if __name__ == '__main__':
    pid = None
    while True:
        pidNotHandle = list(psutil.process_iter())
        pids = []
        path = 'animal_crossing/data/pid.json'
        if os.path.exists(path) is False:
            cmd = "python bot.py"
            os.popen(cmd, 'w')
            print("开启程序.............")
        else:
            info = common.read_json(path, {})
            if info['rebot'] is True:
                print("重启程序.............")
                os.popen('taskkill /f /pid ' + info['pid'])
                cmd = "python bot.py"
                os.popen(cmd, 'w')
            else:
                status = 0
                for each in pidNotHandle:
                    a = str(each)
                    pids.append(a[15:-1])
                    status = 0  # 被监控程序进程存在状态，0不存在，1存在
                for each in pids:
                    nameposition = each.find("name")  # 获取name的位置；name='System Idle Process'
                    namevalue = each[nameposition + 6:-1]  # 获取name值；System Idle Process
                    pidposition = each.find("pid")
                    pidvalue = each[pidposition + 4:nameposition - 2]
                    if pidvalue == info['pid']:
                        status = 1
                        print("发现进程==============name=" + namevalue + ", pid=" + pidvalue + "\n")
                        break
                if status == 0:  # 进程不存在，重新启动程序
                    cmd = "python bot.py"
                    os.popen(cmd, 'w')
                    print("进程不存在，启动程序.............")
        time.sleep(60)
