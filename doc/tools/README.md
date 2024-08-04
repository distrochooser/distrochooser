# Tools

General process: 

1. `migrate.py` creates new `*.toml` and `*.json` files from a given Distrochooser 5 fixture.
2. `translate-dump.py` creates .txt files to be used e. g.  in translation services. It will split the missing translation into a key file and a import file. The script is meant to update missing values. Missing values are filled with the english translation in non-english translation files
3. `translate-import.py` reads the `*_keys.txt` and `*_import.txt` files and merges them with json files from the translations, replacing all english values.
4. Copy the new *.json files into the locales folder 
5. Restart the server