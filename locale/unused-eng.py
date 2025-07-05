from json import dumps, loads
from subprocess import getoutput


file = "./lang-en.json"
data = loads(open(file, "r").read())

def find(what: str):
    cmd = f"grep -i -R '{what}' ../ --include='*.py' --include='*.toml' --include='*.vue' --include='*.ts' --exclude='../venv/*' --exclude='../code/frontend/node_modules/*' --exclude='../cache/*'"
    output = getoutput(cmd)
    return len(output) > 0


# find translations in the leading en translation which are not used in a python, vue, ts nor a toml file.

new_dict = {}

all_keys = list(data.keys())
for key, value in data.items():
    found = False
    number =all_keys.index(key) +1
    with_match = ""
    # at some point, there might be a separate argument list for properties of translatables
    # we don't care what the _actual_ call is, just searching for the prefix here.
    if not found:
        with_match = "description"
        found = find(key.replace("-description", ""))
    if not found:
        with_match = "text"
        found = find(key.replace("-text", ""))
    if not found:
        with_match = "help"
        found = find(key.replace("-help", ""))
    if not found:
        with_match = "title"
        found = find(key.replace("-title", ""))
    if not found:
        with_match="exact"
        found = find(key)
    if not found:
        print(f"Key #: {number}/{all_keys.__len__()} {key} found nowhere.")
    else:
        print(f"Key #: {number}/{all_keys.__len__()} {key} found with match {with_match}!")
        new_dict[key] = value




with open(file, "w") as file:
    file.write(dumps(new_dict, ensure_ascii=False, indent=4).encode("utf-8").decode())
