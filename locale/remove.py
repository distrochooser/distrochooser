from os import listdir
from sys import argv
from json import loads, dumps

if len(argv) != 2:
    raise Exception("Add new value key")

key = argv[1]

locales = listdir(".")

addition = {}

for locale in locales:
    if ".json" in locale:
        contents = ""
        with open(locale, "r") as file:
            contents = file.read()
        data = loads(contents)
        del data[key]
        data = dict(sorted(data.items()))
        with open(locale, "w") as file:
            file.write(
                dumps(data, ensure_ascii=False, indent=4).encode("utf-8").decode()
            )
