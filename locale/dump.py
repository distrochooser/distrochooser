from json import dumps, loads
from sys import argv
from pyperclip import copy

file = "./lang-en.json"
base_translation = loads(open(file, "r").read())

for _, value in base_translation.items():
    print(value.replace("distrochooser", "ABC").replace("Distrochooser", "ABC"))