import json


class Room:
    def __init__(self):
        self.room = {}
        self.member = {}
        self.queue = {}
        self.history = {}
        self.count = {}

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

    def getUserId(self, name):
        self.read("animal_crossing/data/cur.json", "lottery")
        return self.lottery[name][5]

    def open(self, msgList, groupId, userId):
        self.read("room")
        self.read("count")
        self.read("member")
        self.read("queue")
        self.count["count"] = self.count["count"] + 1
        id = self.count["count"]
        self.room[str(id)] = {}
        self.member[str(id)] = {}
        self.member[str(id)]["member"] = []
        self.queue[str(id)] = {}
        self.room[str(id)]["id"] = id
        self.room[str(id)]["passwd"] = msgList[0]
        self.room[str(id)]["price"] = msgList[1]
        self.room[str(id)]["group"] = groupId
        self.room[str(id)]["user"] = userId
        self.write("member")
        self.write("queue")
        self.write("room")
        self.write("count")
        return id

    def addQueue(self, mem, id):
        """Add a member to the queue"""

        self.read("queue")
        if self.queue[str(id)] == {}:
            self.queue[str(id)][str(mem)] = 1
        else:
            self.queue[str(id)][str(mem)] = list(self.queue[str(id)].values())[-1] + 1
            print(self.queue[str(id)][str(mem)])
        self.write("queue")

    def getRoomQueue(self, id):
        """Return the queue number of the last member in target room"""

        self.read("member")
        self.read("queue")
        if self.member[str(id)]["member"] == []:
            return 0
        return self.queue[str(id)][str(self.member[str(id)]["member"][-1])]

    def getQueueNum(self, mem):
        """Return the queue number of mem"""

        self.read("queue")
        for queue in self.queue.values():
            for queueMem in queue.keys():
                if str(mem) == queueMem:
                    return queue[queueMem]
        return None

    def getWaitLen(self, mem):
        """Return the queue length before mem"""

        for id, queue in self.queue.items():
            for queueMem in queue.keys():
                if str(mem) == queueMem:
                    idIN = id
                    num = queue[queueMem]
                    cur = self.getRoomQueue(idIN)
                    return num - cur - 1
        return None

    def getQueueLen(self, id):
        """Return the queue lenth"""

        cur = self.getRoomQueue(id)
        if self.queue[str(id)] == {}:
            return 0
        return list(self.queue[str(id)].values())[-1] - cur

    def exitQueue(self, mem):
        """Exit queue (useless)"""

        self.read("queue")
        for queue in self.queue.values():
            for queueMem in queue.keys():
                if mem == queueMem:
                    del queue[queueMem]
                    return True
        return False

    def close(self, roomID):
        """Close one room"""

        self.read("room")
        self.read("member")
        self.read("history")
        self.read("queue")
        self.history[str(roomID)] = self.room[str(roomID)]
        self.history[str(roomID)]["number"] = len(self.queue[str(roomID)].keys())
        del self.room[str(roomID)]
        del self.member[str(roomID)]
        del self.queue[str(roomID)]
        self.write("queue")
        self.write("room")
        self.write("member")
        self.write("history")


    def addMember(self, mem, id):
        """Add a member to the target room"""

        self.read("member")
        self.member[str(id)]["member"].append(mem)
        self.write("member")

    def exitMem(self, mem, id):
        """Exit room"""

        self.read("member")
        self.member[str(id)]["member"].remove(mem)
        self.write("member")


    def inMember(self, mem):
        """Return the mem's room id"""

        self.read("member")
        for id, memList in self.member.items():
            if mem in memList["member"]:
                return id
        return None

    def getRoom(self):
        self.read("room")
        return

    def getQueue(self):
        self.read("queue")
        return

    def getMember(self):
        self.read("member")
        return

    def getUserNumber(self, id):
        """Return the number of people in the room"""

        self.read("member")
        if self.member[str(id)]["member"] == []:
            return 0
        return len(self.member[str(id)]["member"])

    def getGroupList(self):
        """Get tencent groups list"""

        self.read("room")
        groupList = []
        for value in self.room.values():
            groupList.append(value["group"])
        return groupList

    def toString(self, groupId):
        self.read("room")
        self.read("member")
        self.read("queue")
        output = ''
        groupRoom = {}
        for singleRoom in self.room.values():
            if singleRoom["group"] == groupId:
                groupRoom[singleRoom["id"]] = singleRoom
        if groupRoom == {}:
            output += '当前无房间开放'
        else:
            for room in groupRoom.values():
                id = room["id"]
                output += f"""========================
房间ID：{room["id"]}
房间人数：{self.getUserNumber(id)}
排队人数：{self.getQueueLen(id)}
"""
        return output


