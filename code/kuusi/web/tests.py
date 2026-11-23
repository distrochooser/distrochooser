"""
distrochooser
Copyright (C) 2014-2026 Christoph Müller <distrochooser@chmr.eu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from django.test import SimpleTestCase, TestCase

from web.util import (
    TRANSLATIONS,
    get_translation,
    get_translation_haystack,
    hot_load_translations,
)


class TranslationLoadingTest(SimpleTestCase):
    """locale/lang-*.json must load under their full language codes.

    A code with a subtag (zh-hans, zh-hant) is itself a language key in
    AVAILABLE_LANGUAGES, so it may not collapse onto its primary subtag.
    """

    def test_subtag_languages_load_distinct(self):
        TRANSLATIONS.clear()
        hot_load_translations()
        try:
            self.assertIn("zh-hans", TRANSLATIONS)
            self.assertIn("zh-hant", TRANSLATIONS)
            self.assertNotIn("zh", TRANSLATIONS)
            self.assertEqual(
                get_translation("a11y", "zh-hans"),
                TRANSLATIONS["zh-hans"]["a11y"],
            )
            haystack = get_translation_haystack(TRANSLATIONS, "zh-hans")
            self.assertIn("a11y", haystack)
        finally:
            TRANSLATIONS.clear()
            hot_load_translations()


# Create your tests here.
