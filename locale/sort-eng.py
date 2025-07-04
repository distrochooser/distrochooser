from json import dumps, loads
from subprocess import getoutput


file = "./lang-eng.json"
data = loads(open(file, "r").read())
data = dict(sorted(data.items()))
with open(file, "w") as file:
    file.write(
        dumps(data, ensure_ascii=False, indent=4)
        .encode("utf-8")
        .decode()
    )
