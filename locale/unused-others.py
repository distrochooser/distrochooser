from json import dumps, loads
from os import listdir

file = "./lang-en.json"
data = loads(open(file, "r").read())

for file in listdir():
    if "json" in file:
        if "-en" not in file:
            translation = loads(open(file, "r").read())

            expected_keys = list(data.keys())
            new_translation = {}
            for key in expected_keys:
                if key in translation:
                    new_translation[key] = translation[key]
                else:
                    new_translation[key] = f"!!{data[key]}"
            new_translation = dict(sorted(new_translation.items()))
            with open(file, "w") as file:
                file.write(
                    dumps(new_translation, ensure_ascii=False, indent=4)
                    .encode("utf-8")
                    .decode()
                )
