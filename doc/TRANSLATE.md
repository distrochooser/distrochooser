# How to translate

The application stores all translation inside of *.json files inside of the first path defined within the `settings.py`
`LOCALES_PATH`.

All files follow the format `<scope>-<iso-639-1>.json`. Translations can be updated using the JSON files or can be
updated during runtime.

🚨 If the language is new, add it into the `AVAILABLE_LANGUAGES` list before continuing. Please use the ISO-639-1 codes as first tuple element, followed by an name for the language.

## How to provide translations

There are two ways to translate: Using the _in app translation_ or by updating the JSON files itself.

### In-App-Translation

The app features a button, labelled with "help translation". This button triggers the mode to be able to change
any translatable value within the application. If the data ist stored, the user session will continue use this proposal.

This approach aims to replace the need for third-party tools and services.

### Persist proposals

To persist proposals, the backend CLI interface can be used. the command `python manage.py language` is to be used here with following commands:

-`python manage.py language en` - List all proposals for lang code `en`
- `python manage.py language en --clear` - Delete all proposals
- `python manage.py language en --delete <id>` - Delete a given proposal by it's id
- `python manage.py language en --approve <id>` - Approve given proposals (ID's will be printed on screen by the list command)
- `python manage.py language en --persist` - All approved proposals will be written into files. If the language key is present within the json files, the file will be updated (first hit counts). If not, a file `additional-<langcode>.json` will be read 

> Please note that changes on the json files require a restart

### JSON file update

Translations are stored in `locale/lang-<languagecode>.json`.

The content of all translation files is a JSON dictionary, describing the values. The keys inside the dictionary should be kept lower case.

🚨 All types of translation updates require a restart.

# Tools inside of /locale


- `dump.py`: Dumps the english baseline into stdout, e. g. for machine based translation (e. g. pipe into text file `dump.py > raw.txt`). The script uses `lang-eng.json` as baseline.
- `read.py <lang_code>`: Read the file `raw.txt` (created by `dumpy.py` and translated somewhere else) to generate a `lang-<lang_code>.json` file. The script uses `lang-eng.json` as baseline.
- `fixmissing.py <lang_code>`: Prompts missing values of a given `lang_code` for individual translation.
- `unused-eng.py`: Searchs if a string is most likely unused.  The script uses `lang-eng.json` as baseline.
- `unused-others.py`: Searchs if a string is most likely unused in any translation EXCEPT the english baseline.