from os.path import join, exists
from backend.settings import CONFIG, LOCALES
# not using django's translation model b/c of dynamical content instead of values taken out of the sourcecode
import polib

def parseTranslation(langCode: str, poFile: str) -> dict:
  if langCode not in LOCALES:
    raise Exception("Language not installed")
  po = polib.pofile(poFile)
  result = {}
  for entry in po:
    result[entry.msgid] = entry.msgstr
  return result

# Build the translation one time to prevent them from being generated on each request
TRANSLATIONS = {}
for key, value in LOCALES.items():
  try:
    TRANSLATIONS[key] = parseTranslation(key, value)
  except:
    print(f"ERROR in FILE {key}")


TESTOFFSET = 713037
COMMIT = None
if exists("commit"):
  with open("commit", "r") as file:
    COMMIT = file.read()

print("distrochooser5", COMMIT)