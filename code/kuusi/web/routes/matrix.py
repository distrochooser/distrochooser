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

from django.http import (
    HttpResponse,
    HttpResponseNotAllowed,
    HttpResponseForbidden,
    HttpResponseNotFound,
)
from django.utils.translation import gettext_lazy as _
from django.core.management import call_command
from django.views.decorators.csrf import csrf_exempt
from os.path import join

from kuusi.settings import (
    UPDATE_API_KEY,
    UPDATE_UPLOAD_PATH
)
from web.models import WebHttpRequest
from web.helper import forward_helper
from logging import getLogger

@csrf_exempt
def route_update(request: WebHttpRequest) -> HttpResponse:
    """
    Update the matrix OTA. Has the same logic as manage.py parse <filename>

    The endpoint receives a set of files, which have their original filenames.
    The first file is considered as "main" file and will be used to trigger the parse mechanism.

    The endpoint requires an Authorization header to feature the value from UPDATE_API_KEY and the method must be POST.

    """
    if request.method != "POST":
        return HttpResponseNotAllowed("Not allowed")

    header = request.headers.get("Authorization")

    if not header or header != UPDATE_API_KEY:
        return HttpResponseForbidden("Forbidden")

    if request.FILES.__len__ == 0:
        return HttpResponseNotFound("File is missing")
    first_file_name = None
    for key, file_content in request.FILES.items():
        if not first_file_name:
            first_file_name = key
        with open(join(UPDATE_UPLOAD_PATH, key), "wb") as file:
            for chunk in file_content.chunks():
                file.write(chunk)
    call_command("parse", join(UPDATE_UPLOAD_PATH, first_file_name))
    return HttpResponse("ok")
