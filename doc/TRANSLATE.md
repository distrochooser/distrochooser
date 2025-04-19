# How to translate

The application stores all translation inside of *.json files inside of the first path defined within the `settings.py`
`LOCALES_PATH`.

All files follow the format `<scope>-<iso-639-3>.json`. Translations can be updated using the JSON files or can be
updated during runtime.

## Third party translation.

🚨 If the language is new, add it into the `AVAILABLE_LANGUAGES` list before continuing. Please use the ISO-639-3 codes as first tuple element, followed by an name for the language.

There is the command `translation` to export and import locale values for external translation. It can be called with `python manage.py language <lang_code> <path>`. Invoking this command will create a file `lang_code.txt`  in `path`.
The content can be used in external api's for translation. To read this, drop the translated content into the file again (make sure line amount and order matches) and execute:

`python manage.py language <lang_code> <path> --read`. The file will be read, the locales be updated an the txt file will be removed. There is the option for a dry run without altering files (`--dry_run`). 

🚨 Do not approve or change language values between drop and read of these txt files. Otherwise you will mess up with the ordering.

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

Translations are stored in `locale/<prefix>-<languagecode>.json`, while the `prefix` just serves for grouping purposes, but can be omitted with using `additional` as prefix. For example, if you creaete a japanese translation, you can use `locale/additional-jpn.json` as a file name.

The content of all translation files is a JSON dictionary, describing the values.

🚨 All types of translation updates require a restart.