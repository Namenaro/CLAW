
import json
import jsonpickle
from json import JSONEncoder


class MyClass:
    def __init__(self):
        self.x = 5
        self.y = 4

    def __str__(self):
        return str(self.x)+"_"+str(self.y)


class Second:
    def __init__(self):
        self.my = MyClass()

    def __str__(self):
        return "Second has" + str(self.my)


if __name__ == '__main__':
    obj = Second()
    frozen = jsonpickle.encode(obj)

    with open("data_file1.json", "w") as write_file:
        write_file.write(frozen)

    with open("data_file1.json", "r") as read_file:
        loaded = read_file.read()
        thawed = jsonpickle.decode(loaded)
        print(str(thawed))

