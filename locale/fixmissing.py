from json import dumps, loads
from sys import argv
from pyperclip import copy

file = "./lang-eng.json"
base_translation = loads(open(file, "r").read())


lang_code = argv[1]
file = f"./lang-{lang_code}.json"
target_translation = loads(open(file, "r").read())


for key in base_translation:
    try:
        value = target_translation[key]
        if "!!" in value or value == base_translation[key]:
            input_value = value.replace('!!', '').replace("distrochooser", "ABC").replace("Distrochooser", "ABC")
            copy(input_value)
            got = input(f"Get value for: {key}: {input_value}: ")
            if "ABC" in got:
                got = got.replace("ABC", "Distrochooser")
            if got:
                target_translation[key] = got
    except KeyboardInterrupt:
        break

with open(file, "w") as file:
    file.write(
        dumps(target_translation, ensure_ascii=False, indent=4)
        .encode("utf-8")
        .decode()
    )
