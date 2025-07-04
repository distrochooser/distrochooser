from os import listdir, unlink
from json import loads, dumps


files = listdir(".")

for file in files:
    if f".json" in file:

        content = open(file).read()
        json_obj = loads(content)
        new_obj = {}
        for key, value in json_obj.items():
            key = key.lower()
            new_obj[key] = value

        with open(file, "w") as file:
            file.write(dumps(new_obj, skipkeys=True, allow_nan=True, indent=6))

        