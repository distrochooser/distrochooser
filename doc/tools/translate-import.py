from os.path import join,exists
from os import listdir
from json import loads, dumps


LOCALES_PATH = "../../locale"
SOURCE_PATH = "../../locale-pipeline"
RESULTS_PATH = "../../locale-pipeline-results"

files = listdir(LOCALES_PATH)
source_files = listdir(SOURCE_PATH)
locales = {}


for file in files:
    if ".json" in file:
        parts = file.split("-")
        lang = parts[1].split(".")[0]
        if lang not in locales:
            locales[lang] = {}
        locales[lang][file] = loads(open(join(LOCALES_PATH, file)).read())

new_values = {}
for file in source_files:
    if "_keys" in file:
        lang_code = file.split("_")[0]
        new_values[lang_code] = {}
        
        keys = open(join(SOURCE_PATH, file)).readlines()
        import_path = join(SOURCE_PATH, lang_code + "_import.txt")
        if exists(import_path):
            print(import_path)
            values = open(import_path).readlines()
            for index, key in enumerate(keys):
                key_value = key.strip("\n")
                value_value = values[index].strip("\n")
                new_values[lang_code][key_value] = value_value.replace("SERVICENAME", "Distrochooser")
            
            print(f"Collected {len( new_values[lang_code])} for lang code {lang_code}.")


for lang_code, files in locales.items():
    if lang_code != "en" and lang_code in new_values:
        new_values_lang = new_values[lang_code]
        for file_name, content in files.items():
            print(f"processing {file_name}")
            needs_update = False
            for key, value in content.items():
                if key in new_values_lang:
                    new_value = new_values_lang[key]
                    print(f"Replacing {key} with value {new_value}")
                    files[file_name][key] = new_value
                    needs_update = True
            if needs_update:
                new_path = join(RESULTS_PATH, file_name)
                with open(new_path, "w") as file:
                    file.write(dumps( files[file_name], indent=4))