from os import path, getpid
import nonebot
import config
import json
# import os
# import logging.config

if __name__ == '__main__':
    fo = open('animal_crossing/data/pid.json', "w")
    fo.write(json.dumps({'pid': str(getpid()), 'rebot': False}))
    fo.flush()
    fo.close()

    # config_path = 'logging.json'
    # if os.path.exists(config_path):
    #     with open(config_path, "r") as f:
    #         log_config = json.load(f)
    #         logging.config.dictConfig(log_config)

    nonebot.init(config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'animal_crossing', 'plugins'),
        'animal_crossing.plugins'
    )
    nonebot.run(host="127.0.0.1", port=8081)
