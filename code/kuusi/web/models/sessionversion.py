"""
kuusi
Copyright (C) 2014-2024  Christoph Müller  <mail@chmr.eu>

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

from web.models import Translateable, TranslateableField, Widget, SessionMeta
from django.template import loader
from django.apps import apps

class SessionVersion(Translateable):
    version_name = TranslateableField(null=False, blank=False, max_length=120)


# TODO: Make this proper enums to use in a11y_classes() as well
# TODO: Merge A11Y_OPTIONS and A11Y_KEYS into one structure
A11Y_OPTIONS = {
    "font": {
        "DEFAULT": "FONT_SIZE_DEFAULT",
        "LARGER": "FONT_SIZE_LARGER",
        "LARGEST": "FONT_SIZE_LARGEST"
    }
}

A11Y_KEYS = [
    "COLOR_MODE_BLACK_AND_WHITE"
]

class SessionVersionWidget(Widget):
    def proceed(self, request, page) -> bool:
        session = request.session_obj
        version = request.POST.get("KU_SESSION_VERSION")

        if session:
            if version is None or len(version) == 0:
                session.version = None
            else:
                session.version = SessionVersion.objects.get(pk=version)
            session.save()
        
        
        had_a11y_modes_set = self.proceed_a11y(request, session)
        return not had_a11y_modes_set
    
    def proceed_a11y(self, request, session) -> bool:
        """
        Saves the a11y flags. 

        Returns
            If new modes were selected true, otherwise false
        """
        font_size = request.POST.get("FONT_SIZE") 

        SessionMeta.objects.filter(session=session).delete()
        meta = SessionMeta(
            session = session,
            meta_key = "FONT_SIZE",
            meta_value = font_size
        )
        meta.save()

        mode_needles = A11Y_KEYS
        active_modes = [n in request.POST.keys() for n in mode_needles]
        for index, needle in enumerate(mode_needles):
            active = active_modes[index]
            if active:
                had_changed = True
                meta = SessionMeta(
                    session = session,
                    meta_key = needle,
                    meta_value = "True"
                )
                meta.save()
        return False
    
    def render(self, request, page):
        render_template = loader.get_template(f"widgets/version.html")
        versions = apps.get_model("web", "SessionVersion").objects.filter(is_invalidated=False)
        metas = SessionMeta.objects.filter(session=request.session_obj)
        active_a11y = {}

        for section, options in A11Y_OPTIONS.items():
            active_a11y[section] = {}
            for key, value in options.items():
                active_a11y[section][key] = metas.filter(meta_value=value).count() > 0
        active_a11y["others"] =  {}
        for key in A11Y_KEYS:
            active_a11y["others"][key] = metas.filter(meta_key=key).count() > 0
        return render_template.render(
            {
                "versions": versions,
                "a11y_options": A11Y_OPTIONS,
                "a11y_keys": A11Y_KEYS,
                "selected_version": None
                if not request.session_obj
                else request.session_obj.version,
                "active_a11y": active_a11y,
                "language_code": request.session_obj.language_code
            },
            request,
        )