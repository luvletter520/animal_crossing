import json
import operator

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

    def sort(self, dict):
        """Return a sorted dict"""

        sorted_d = dict( sorted(dict.items(), key=operator.itemgetter(1)))
        return sorted_d

    def addPrice(self, group, user, price):
        """Add a price to the list"""

        user = str(user)
        group = str(group)
        self.read("price")
        if group not in self.price.keys():
            self.price[group] = {}
        self.price[group][user] = price
        self.price[group] = self.sort(self.price[group])
        self.write("price")

    def delPrice(self, group, user):
        """Del the price of user from the list"""

        user = str(user)
        self.read("price")
        self.read("history")
        if group not in self.history.keys():
            self.history[group] = {}
        self.history[group].setdefault(user, []).append(self.price[group][user])
        del self.price[group][user]
        self.write("price")
        self.write("history")

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
        for user, price in groupList.items():
            output += f"""========================
用户ID：{user}
价格：{price}
"""
        return output
