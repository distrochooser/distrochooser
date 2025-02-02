"""
distrochooser
Copyright (C) 2014-2025  Christoph Müller  <mail@chmr.eu>

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

from django.http import HttpResponse
from web.models import WebHttpRequest
from kuusi.settings import LANGUAGE_CODES, ROBOTS_TXT, SITEMAP_ADDITIONAL_ENTRIES, SITEMAP_PUBLIC_URL

def route_robots_txt(_: WebHttpRequest):

    for user_agent, rules in ROBOTS_TXT.items():
        robots_content = f"User-agent: {user_agent}\n"
        for rule in rules:
            if "language_code" in rule:
                for code in LANGUAGE_CODES:
                    rule_content = rule.replace("language_code", code)
                    robots_content += f"Disallow: {rule_content}\n"
            else:
                robots_content += f"Disallow: {rule}\n"

    
    response =  HttpResponse(robots_content)
    response.headers["content-type"] = "text/plain"

    return response

def route_sitemap_xml(_: WebHttpRequest):
    xml_content = "<urlset>"

    # Add all root pages
    for language_code in LANGUAGE_CODES:
        xml_content += f"<url><loc>{SITEMAP_PUBLIC_URL}/{language_code}</loc></url>"

    # Add all additional records
    for entry in SITEMAP_ADDITIONAL_ENTRIES:
        if "language_code" in entry:
            for language_code in LANGUAGE_CODES:
                entry_content = entry.replace("language_code", language_code)
                xml_content += f"<url><loc>{SITEMAP_PUBLIC_URL}{entry_content}</loc></url>"
        else:
            xml_content += f"<url><loc>{SITEMAP_PUBLIC_URL}{entry}</loc></url>"



    xml_content += "</urlset>"

    response =  HttpResponse(xml_content)
    response.headers["content-type"] = "application/xml"

    return response