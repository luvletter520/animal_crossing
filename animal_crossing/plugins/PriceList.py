import json
import common
import time


class Price:

    def __init__(self):
        self.price = {}
        self.history = {}

    def read(self, var):
        if var == "price":
            fo = open("animal_crossing/data/price.json")
            self.price = json.load(fo)
        elif var == "history":
            fo = open("animal_crossing/data/price_history.json")
            self.history = json.load(fo)
        fo.close()

    def write(self, var):
        if var == "price":
            fo = open("animal_crossing/data/price.json", "w")
            j = json.dumps(self.price)
        elif var == "history":
            fo = open("animal_crossing/data/price_history.json", "w")
            j = json.dumps(self.history)
        fo.write(j)
        fo.close()

    def sort(self, dic, reverse=True):
        """Return a sorted dict"""

        sorted_d = dict(sorted(dic.items(), key=lambda x: x[1]['price'], reverse=reverse))
        return sorted_d

    def addPrice(self, group, user, nickname, price):
        """Add a price to the list"""

        user = str(user)
        group = str(group)
        nickname = str(nickname)
        self.read("price")
        if group not in self.price.keys():
            self.price[group] = {}
        self.price[group][user] = {'price': price, 'nickname': nickname, 'time': time.time()}
        self.price[group] = self.sort(self.price[group], common.is_sunday() is False)
        self.write("price")

    def delPrice(self, group, user):
        """Del the price of user from the list"""

        user = str(user)
        self.read("price")
        del self.price[group][user]
        self.write("price")

    def delAll(self):
        """Del all prices"""

        self.read("price")
        self.read("history")
        for k, v in self.price.items():
            for user, list in v.items():
                if k not in self.history.keys():
                    self.history[k] = {}
                self.history[k].setdefault(user, []).append(self.price[k][user])
            self.price[k] = {}
        self.write("price")
        self.write("history")

    def getGroupList(self):
        """Get tencent groups list"""

        self.read("price")
        groupList = []
        for k, v in self.price.items():
            if v != {}:
                groupList.append(k)
        return groupList

    def getPriceList(self):
        self.read("price")
        return self.price

    def toString(self, group):

        group = str(group)
        self.read("price")
        self.read("history")
        output = ""
        groupList = {}
        for key, value in self.price.items():
            if group == key:
                groupList = value
        for user, info in groupList.items():
            output += f"""========================
QQ号：{user}
昵称：{info['nickname']}
价格：{info['price']}"""
        return output
