from os.path import join
from backend.settings import LOCALES
# not using django's translation model b/c of dynamical content instead of values taken out of the sourcecode
import polib

def parseTranslation(langCode: str) -> dict:
  if langCode not in LOCALES:
    raise Exception("Language not installed")

  po = polib.pofile(LOCALES[langCode])
  result = {}
  for entry in po:
    result[entry.msgid] = entry.msgstr
  return result


# Build the translation one time to prevent them from being generated on each request
TRANSLATIONS = {
  "en": parseTranslation("en"),
  "de": {}
}

TESTOFFSET = 652949  