import json
import time
import config


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
        self.history = {}
        self.count = {}
        self.read("room")
        self.read("count")
        self.read("member")
        self.read("queue")
        self.read("history")

    def claerAll(self):
        self.room = {}
        self.member = {}
        self.queue = {}
        self.history = {}
        self.count = {"count": 0}
        self.save()

    def read(self, var):
        if var == "room":
            fo = open("animal_crossing/data/room.json")
            self.room = json.load(fo)
        elif var == "member":
            fo = open("animal_crossing/data/member.json")
            self.member = json.load(fo)
        elif var == "history":
            fo = open("animal_crossing/data/history.json")
            self.history = json.load(fo)
        elif var == "count":
            fo = open("animal_crossing/data/count.json")
            self.count = json.load(fo)
        elif var == "queue":
            fo = open("animal_crossing/data/queue.json")
            self.queue = json.load(fo)
        fo.close()

    def write(self, var):
        if var == "room":
            fo = open("animal_crossing/data/room.json", "w")
            j = json.dumps(self.room)
        elif var == "member":
            fo = open("animal_crossing/data/member.json", "w")
            j = json.dumps(self.member)
        elif var == "history":
            fo = open("animal_crossing/data/history.json", "w")
            j = json.dumps(self.history)
        elif var == "count":
            fo = open("animal_crossing/data/count.json", "w")
            j = json.dumps(self.count)
        elif var == "queue":
            fo = open("animal_crossing/data/queue.json", "w")
            j = json.dumps(self.queue)
        fo.write(j)
        fo.close()

    def save(self):
        self.write("member")
        self.write("queue")
        self.write("room")
        self.write("count")

    def open(self, msgList, groupId, userId, nickname, length=config.DEFAULT_CAPACITY):
        self.count["count"] = self.count["count"] + 1
        id = self.count["count"]
        self.room[str(id)] = {}
        self.member[str(id)] = {}
        self.member[str(id)] = {}
        self.queue[str(id)] = {}
        self.room[str(id)]["id"] = id
        self.room[str(id)]["passwd"] = msgList[0]
        self.room[str(id)]["price"] = msgList[1]
        self.room[str(id)]["group"] = groupId
        self.room[str(id)]["user"] = userId
        self.room[str(id)]["nickname"] = nickname
        self.room[str(id)]["length"] = int(length)
        self.room[str(id)]["time"] = time.time()
        return id

    def reopen(self, roomId, passwd, length=None):
        self.room[roomId]["passwd"] = passwd
        if length:
            self.room[roomId]["length"] = int(length)
        return id

    def addQueue(self, mem, id, nickname):
        """Add a member to the queue"""
        self.queue[str(id)][str(mem)] = {'time': time.time(), 'nickname': nickname}

    def getWaitLen(self, mem):
        mem = str(mem)
        """Return the queue length before mem"""
        for id, queue in self.queue.items():
            count = 1
            for queueMem in queue.keys():
                if mem == queueMem:
                    return count
                count += 1
        return None

    def getQueueLen(self, id):
        """Return the queue lenth"""

        id = str(id)
        count = 0
        for i in self.queue[id]:
            count += 1
        return count

    def close(self, roomID):
        """Close one room"""

        self.history[str(roomID)] = self.room[str(roomID)]
        self.history[str(roomID)]["number"] = len(self.queue[str(roomID)])
        del self.room[str(roomID)]
        del self.member[str(roomID)]
        del self.queue[str(roomID)]

    def addMember(self, mem, id, nickname, ready=True):
        """Add a member to the target room"""
        self.member[str(id)][str(mem)] = {'time': time.time(), 'ready': ready, 'nickname': nickname}

    def exitMem(self, mem, id):
        """Exit room"""
        if str(id) in self.member:
            if str(mem) in self.member[str(id)]:
                del self.member[str(id)][str(mem)]

    def exitQueue(self, mem, id):
        """Exit queue"""

        del self.queue[str(id)][str(mem)]

    def inMember(self, mem):
        """Return the mem's room id"""

        for id, memList in self.member.items():
            if str(mem) in memList.keys():
                return id
        return None

    def inQueue(self, mem):
        """Return the mem's queue id"""

        for id, memList in self.queue.items():
            if str(mem) in memList.keys():
                return id
        return None

    def getUserNumber(self, id):
        """Return the number of people in the room"""
        if self.member[str(id)] is []:
            return 0
        return len(self.member[str(id)])

    def getGroupList(self):
        """Get tencent groups list"""

        groupList = []
        for value in self.room.values():
            groupList.append(value["group"])
        return groupList

    def toString(self, groupId):
        output = ''
        groupRoom = {}
        for singleRoom in self.room.values():
            if singleRoom["group"] == groupId:
                groupRoom[singleRoom["id"]] = singleRoom
        if groupRoom == {}:
            output += '当前暂无岛开门'
        else:
            for room in groupRoom.values():
                id = room["id"]
                output += f"""========================
岛ID：{room["id"]}
岛主QQ号：{room['user']}
岛主QQ昵称：{room['nickname']}
白菜头价格：{room["price"]}
最大登岛人数为：{room["length"]}
岛上人数：{self.getUserNumber(id)}
排队人数：{self.getQueueLen(id)}
"""
        return output
