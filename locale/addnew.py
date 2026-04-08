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
        if key not in data:
            got = input(f"Add translation for locale={locale} key={key}: ")
            if got != "":
                addition[locale] = got
        else:
            print(f"Skipping locale={locale} as key={key} is already present")

for locale_key, value in addition.items():
    contents = ""
    with open(locale_key, "r") as file:
        contents = file.read()
    
    data = loads(contents)
    data[key] = value

    data = dict(sorted(data.items()))
    with open(locale_key, "w") as file:
        file.write(
            dumps(data, ensure_ascii=False, indent=4)
            .encode("utf-8")
            .decode()
        )