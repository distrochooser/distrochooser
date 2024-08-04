from json import loads
from os import listdir
from os.path import join

LOCALES_PATH = "../../locale"
TARGET_PATH = "../../locale-pipeline"

locales={}
files = listdir(LOCALES_PATH)

for file in files:
    if ".json" in file:
        parts = file.split("-")
        lang = parts[1].split(".")[0]
        if lang not in locales:
            locales[lang] = []
        locales[lang].append(file)

reference = {}

for lang_code, lang_files in locales.items():
    print(lang_code)
    if lang_code == "en":
        for lang_file in lang_files:
            file_prefix = lang_file.split("-")[0]
            reference[file_prefix] = loads(open(join(LOCALES_PATH, lang_file), "r").read())

for lang_code, lang_files in locales.items():
    if lang_code != "en":
        path = join(TARGET_PATH, lang_code + ".txt")
        key_path = join(TARGET_PATH, lang_code + "_keys.txt")
        content = ""
        key_content = ""
        for lang_file in lang_files:
            file_prefix = lang_file.split("-")[0]
            file_content = loads(open(join(LOCALES_PATH, lang_file), "r").read())
            for key, value in file_content.items():
                if value is not None and value == reference[file_prefix][key] and "-name" not in key: # don't translate none values and distro names
                    content += value + "\n"
                    key_content += key + "\n"
        
        content = content.replace("Distrochooser.de", "SERVICENAME")
        with open(path, "w") as file:
            file.write(f"{content}")
        with open(key_path, "w") as file:
            file.write(f"{key_content}")
