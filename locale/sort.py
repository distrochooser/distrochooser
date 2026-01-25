from os import listdir
from json import loads, dumps

files = listdir("./")

for file in files:
    if file.endswith(".json"):
        data = None
        with open(file, "r") as handle:
            data = loads(handle.read())
            print(data)
        data = dict(sorted(data.items()))   
        with open(file, "w") as handle:
            handle.write(
                dumps(
                    data, ensure_ascii=False, indent=4
                )
            )
