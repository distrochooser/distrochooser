"""
kuusi
Copyright (C) 2014-2023  Christoph Müller <mail@chmr.eu>

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

from web.models import Translateable, TranslateableField, Widget

from django.template import loader
from django.apps import apps

class SessionVersion(Translateable):
    version_name = TranslateableField(null=False, blank=False, max_length=120)


class SessionVersionWidget(Widget):
    def proceed(self, request, page) -> bool:
        # TODO: Force the page to run into an exception if the page afterwards is not requiring a session.

        session = request.session_obj
        version = request.POST.get("KU_SESSION_VERSION")

        if session:
            if version is None or len(version) == 0:
                session.version = None
            else:
                session.version = SessionVersion.objects.get(pk=version)
            session.save()
        return True

    def render(self, request, page):
        render_template = loader.get_template(f"widgets/version.html")
        versions = apps.get_model("web", "SessionVersion").objects.filter(is_invalidated=False)
        return render_template.render(
            {
                "versions": versions,
                "selected_version": None
                if not request.session_obj
                else request.session_obj.version,
            },
            request,
        )