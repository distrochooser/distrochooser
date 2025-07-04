from json import dumps, loads
from os import listdir


files = listdir()

for file in files:
    print(file)
    if ".json" in file:
        data = loads(open(file, "r").read())

        with open(file, "w") as file:
            file.write(dumps(data, ensure_ascii=False, indent=4).encode("utf-8").decode())