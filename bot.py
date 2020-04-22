from os import path, getpid
import nonebot
import config
import json

if __name__ == '__main__':
    fo = open('animal_crossing/data/pid.json', "w")
    fo.write(json.dumps({'pid': str(getpid()), 'rebot': False}))
    fo.flush()
    fo.close()

    nonebot.init(config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'animal_crossing', 'plugins'),
        'animal_crossing.plugins'
    )
    nonebot.run()
