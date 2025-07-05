from sys import argv
from json import loads, dumps

lang_code = argv[1]

file = "./lang-en.json"
base_translation = loads(open(file, "r").read())
translation = open("raw.txt", "r").readlines()

base_translation = dict(sorted(base_translation.items()))

new_dict = {}
line = 0
for key, value in base_translation.items():
    new_value = translation[line].strip().replace("ABC", "Distrochooser")
    print(f"{key} => {value} => {new_value}")
    new_dict[key] = new_value

    line += 1
new_dict = dict(sorted(new_dict.items()))

with open(f"lang-{lang_code}.json", "w") as file:
    file.write(
        dumps(new_dict, ensure_ascii=False, indent=4)
        .encode("utf-8")
        .decode()
    )
