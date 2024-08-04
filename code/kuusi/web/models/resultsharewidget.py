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

from web.models import Widget, WebHttpRequest, Page
from django.template import loader

from kuusi.settings import KUUSI_URL

class ResultShareWidget(Widget):
    def proceed(self, request: WebHttpRequest, page: Page) -> bool:
        return True

    def render(self, request: WebHttpRequest, page: Page):
        render_template = loader.get_template(f"widgets/result_share.html")
        return render_template.render(
            {
                "session": request.session_obj,
                "page": page,
                "language_code": request.session_obj.language_code,
                "share_link": f"{KUUSI_URL}/{request.session_obj.language_code}/{request.session_obj.result_id}",
            },
            request,
        )