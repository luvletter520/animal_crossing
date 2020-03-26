import json

test = {}

def write(var):
    if var == "count":
        fo = open("animal_crossing/data/count.json", "w")
        j = json.dumps(test)
    fo.write(j)
    fo.close()

if __name__ == '__main__':
    test["count"] = 0
    write("count")