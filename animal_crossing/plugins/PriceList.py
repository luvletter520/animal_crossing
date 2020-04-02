import json
import common
import time
import threading


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


@singleton
class Price:

    def __init__(self):
        self.price = {}
        self.history = {}
        self.read("price")
        self.read("history")

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(Price, "_instance"):
            Price._instance = Price(*args, **kwargs)
        return Price._instance

    def claerAll(self):
        self.price = {}
        self.history = {}
        self.save()

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

    def save(self):
        self.write('price')
        self.write('history')

    def sort(self, dic, reverse=True):
        """Return a sorted dict"""

        sorted_d = dict(sorted(dic.items(), key=lambda x: x[1]['price'], reverse=reverse))
        return sorted_d

    def addPrice(self, group, user, nickname, price):
        """Add a price to the list"""

        user = str(user)
        group = str(group)
        nickname = str(nickname)
        if group not in self.price.keys():
            self.price[group] = {}
        self.price[group][user] = {'price': price, 'nickname': nickname, 'time': time.time()}
        self.price[group] = self.sort(self.price[group], common.is_sunday() is False)

    def delPrice(self, group, user):
        """Del the price of user from the list"""

        user = str(user)
        del self.price[group][user]

    def delAll(self):
        """Del all prices"""

        for k, v in self.price.items():
            for user, list in v.items():
                if k not in self.history.keys():
                    self.history[k] = {}
                self.history[k].setdefault(user, []).append(self.price[k][user])
            self.price[k] = {}

    def getGroupList(self):
        """Get tencent groups list"""

        groupList = []
        for k, v in self.price.items():
            if v != {}:
                groupList.append(k)
        return groupList

    def getPriceList(self):
        return self.price

    def toString(self, group):

        group = str(group)
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
