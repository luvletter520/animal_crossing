import json
import time
import config
import common
from nonebot import get_bot


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


@singleton
class Room:
    def __init__(self):
        self.room = {}
        self.member = {}
        self.queue = {}
        self.ban = {}
        self.count = {}
        self.group_member = {}
        self.read("room")
        self.read("count")
        self.read("member")
        self.read("queue")
        self.read("ban")
        self.read("group_member")

    def clear_all(self):
        self.room = {}
        self.member = {}
        self.queue = {}
        self.count = {"count": 0}
        self.save()

    def clear_turnip_room(self):
        room_list = self.room.copy()
        for key, room in room_list.items():
            if room['turnip'] is True:
                room_id = str(key)
                del self.room[room_id]
                del self.member[room_id]
                del self.queue[room_id]

    async def check_group_member(self, user_id):
        try:
            if user_id in config.SUPERUSERS:
                return user_id
            bot = get_bot()
            member = await bot.get_group_member_info(group_id=config.GROUP_ID, user_id=user_id)
            return member
        except Exception as e:
            return None

    def read(self, var):
        if var == "room":
            self.room = common.read_json("animal_crossing/data/room.json", {})
        elif var == "member":
            self.member = common.read_json("animal_crossing/data/member.json", {})
        elif var == "ban":
            self.ban = common.read_json("animal_crossing/data/ban.json", {})
        elif var == "count":
            self.count = common.read_json("animal_crossing/data/count.json", {"count": 0})
        elif var == "queue":
            self.queue = common.read_json("animal_crossing/data/queue.json", {})
        elif var == "group_member":
            self.group_member = common.read_json("animal_crossing/data/group_member.json", {})

    def write(self, var):
        if var == "room":
            fo = open("animal_crossing/data/room.json", "w")
            j = json.dumps(self.room)
        elif var == "member":
            fo = open("animal_crossing/data/member.json", "w")
            j = json.dumps(self.member)
        elif var == "ban":
            fo = open("animal_crossing/data/ban.json", "w")
            j = json.dumps(self.ban)
        elif var == "count":
            fo = open("animal_crossing/data/count.json", "w")
            j = json.dumps(self.count)
        elif var == "queue":
            fo = open("animal_crossing/data/queue.json", "w")
            j = json.dumps(self.queue)
        elif var == "group_member":
            fo = open("animal_crossing/data/group_member.json", "w")
            j = json.dumps(self.group_member)
        else:
            return
        fo.write(j)
        fo.close()

    def save(self):
        self.write("member")
        self.write("queue")
        self.write("room")
        self.write("count")
        self.write("ban")

    def open(self, passwd, remake, price, group_id, user_id, nickname, length=config.DEFAULT_CAPACITY):
        self.count["count"] = self.count["count"] + 1
        room_id = self.count["count"]
        self.room[str(room_id)] = {}
        self.member[str(room_id)] = {}
        self.member[str(room_id)] = {}
        self.queue[str(room_id)] = {}
        self.room[str(room_id)]["id"] = room_id
        self.room[str(room_id)]["passwd"] = passwd.upper()
        if price is None:
            self.room[str(room_id)]["remake"] = remake.strip()
            self.room[str(room_id)]["turnip"] = False
        else:
            self.room[str(room_id)]["price"] = price
            self.room[str(room_id)]["turnip"] = True
        self.room[str(room_id)]["group"] = group_id
        self.room[str(room_id)]["user"] = user_id
        if user_id in self.group_member.keys():
            nickname = self.group_member[user_id]['name']
        self.room[str(room_id)]["nickname"] = nickname
        self.room[str(room_id)]["length"] = int(length)
        self.room[str(room_id)]["time"] = time.time()
        return room_id

    def reopen(self, room_id, passwd, length=None):
        self.room[room_id]["passwd"] = passwd
        if length:
            self.room[room_id]["length"] = int(length)
        return room_id

    def add_queue(self, mem, room_id, nickname):
        """Add a member to the queue"""
        mem = str(mem)
        if mem in self.group_member.keys():
            nickname = self.group_member[mem]['name']
        self.queue[str(room_id)][mem] = {'time': time.time(), 'nickname': nickname}

    def get_wait_len(self, mem):
        mem = str(mem)
        """Return the queue length before mem"""
        for queue_id, queue in self.queue.items():
            count = 1
            for queueMem in queue.keys():
                if mem == queueMem:
                    return count
                count += 1
        return None

    def get_queue_len(self, room_id):
        """Return the queue lenth"""
        return len(self.queue[str(room_id)].keys())

    def close(self, room_id):
        """Close one room"""
        del self.room[str(room_id)]
        del self.member[str(room_id)]
        del self.queue[str(room_id)]

    def add_member(self, mem, room_id, nickname, ready=True):
        mem = str(mem)
        if mem in self.group_member.keys():
            nickname = self.group_member[mem]['name']
        """Add a member to the target room"""
        self.member[str(room_id)][str(mem)] = {'time': time.time(), 'ready': ready, 'nickname': nickname}

    def exit_mem(self, mem, room_id):
        """Exit room"""
        if str(room_id) in self.member:
            if str(mem) in self.member[str(room_id)]:
                del self.member[str(room_id)][str(mem)]

    def exit_queue(self, mem, room_id):
        """Exit queue"""
        del self.queue[str(room_id)][str(mem)]

    def in_member(self, mem):
        """Return the mem's room id"""
        for member_id, member_list in self.member.items():
            if str(mem) in member_list.keys():
                return member_id
        return None

    def in_queue(self, mem):
        """Return the mem's queue id"""
        for queue_id, member_list in self.queue.items():
            if str(mem) in member_list.keys():
                return queue_id
        return None

    def get_user_number(self, id):
        """Return the number of people in the room"""
        if self.member[str(id)] is []:
            return 0
        return len(self.member[str(id)])

    def to_string(self, group_id, room_id=None, is_concise=False):
        output = ''
        group_room = []
        for room in self.room.values():
            if room["group"] == group_id and room_id is None:
                group_room.append(room)
            elif room_id == room["id"]:
                group_room.append(room)
        if len(group_room) == 0:
            output += '当前暂无岛开门'
        else:
            i = 0
            is_concise = len(group_room) > 1 and is_concise
            for room in group_room:
                if i > 0:
                    output += '\n========================\n'
                output += self.room_to_string(room, is_concise)
                i += 1
        return output

    def room_to_string(self, room, is_concise):
        room_id = room["id"]
        if room['turnip'] is True and is_concise is False:
            return f"""岛ID：{room["id"]}
岛主QQ号：{room['user']}
岛主QQ昵称：{room['nickname']}
大菜头价格：{room["price"]}
最大登岛人数为：{room["length"]}
岛上人数：{self.get_user_number(room_id)}
排队人数：{self.get_queue_len(room_id)}"""
        if room['turnip'] is True and is_concise is True:
            return f"""岛ID：{room["id"]}
岛主QQ昵称：{room['nickname']}
大菜头价格：{room["price"]}"""
        if room['turnip'] is False and is_concise is True:
            return f"""岛ID：{room["id"]}
岛主QQ昵称：{room['nickname']}
备注：{room["remake"]}"""
        else:
            return f"""岛ID：{room["id"]}
岛主QQ号：{room['user']}
岛主QQ昵称：{room['nickname']}
备注：{room["remake"]}
最大登岛人数为：{room["length"]}
岛上人数：{self.get_user_number(room_id)}
排队人数：{self.get_queue_len(room_id)}"""

    async def next_member(self, room_id):
        bot = get_bot()
        queue_ids = list(self.queue[room_id].keys())
        if len(queue_ids) > 0 and self.get_user_number(room_id) < int(self.room[room_id]['length']):
            user = queue_ids[0]
            self.add_member(user, room_id, self.queue[room_id][user]['nickname'], False)
            self.exit_queue(user, room_id)
            await bot.send_msg(message_type="private",
                               user_id=int(user),
                               message=common.read_format(room_id))
            if len(queue_ids) > 1:
                user = queue_ids[1]
                await bot.send_msg(message_type="private",
                                   user_id=int(user),
                                   message="你当前在排队队伍第一位，下一位就轮到你了，请提前做好登岛准备，如岛上成员长时间未退出房间，可以选择在群里@TA或私聊TA。")
