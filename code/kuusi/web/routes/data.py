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


from django.http import Http404
from django.http import HttpResponse
from django.core.cache import cache
from time import time

from web.models.http import WebHttpRequest
from web.models import Choosable, Session, SessionMeta, Feedback
from web.templatetags.web_extras import _i18n_get_value
from web.opendata import OpenDataV1
from kuusi.settings import SESSION_NUMBER_OFFSET

from user_agents import parse

from json import dumps


def data_v1():
    cached =  cache.get(f"data-access-v1")
    json_data = None
    if cached:
        json_data = cached
    else:
        data = OpenDataV1()
        choosables = Choosable.objects.all()
        choosable: Choosable
        for choosable in choosables:
            data.ChoosableClicks[_i18n_get_value("en", choosable, "name")["value"]] = choosable.clicked

        sessions = Session.objects.all()
        data.Tests = sessions.count()
        data.TestsAllVersions = data.Tests + SESSION_NUMBER_OFFSET
        data.FinishedTests = sessions.filter(is_ack=True).count()
        data.TestsFromOthers = sessions.filter(session_origin__isnull=False).count()

        
        for session in sessions:
            if session.user_agent:
                try:
                    parsed = parse(session.user_agent)
                    if parsed.os.family  not in data.OS_Families:
                        data.OS_Families[parsed.os.family] = 0
                    data.OS_Families[parsed.os.family] += 1
                    if parsed.browser.family  not in data.Browser_Families:
                        data.Browser_Families[parsed.browser.family] = 0
                    data.Browser_Families[parsed.browser.family] += 1
                    if parsed.is_bot:
                        if session.user_agent not in data.Bots:
                            data.Browser_Families[session.user_agent] = 0
                        data.Bots[session.user_agent] += 1
                except:
                    pass # do nothing
                
        feedbacks = Feedback.objects.all()

        for feedback in feedbacks:
            
            cat_id = feedback.assignment.catalogue_id
            if cat_id not in data.FeedbackGivenFlaggedAssignments:
                data.FeedbackGivenFlaggedAssignments[cat_id] = 0
            data.FeedbackGivenFlaggedAssignments[cat_id] += 1


        data.FeedbackGiven = feedbacks.count()
        data.NextUpdate = int(time() + data.RefreshInterval)
        json_data = dumps(data, default=vars)
        data.IsCached = True
        cached_json = dumps(data, default=vars)
        cache.set(f"data-access-v1", cached_json, data.RefreshInterval)


   
    response = HttpResponse(
        content=json_data
    )
    response.headers["Content-Type"] = "application/json"
  
    return response

def route_data(request: WebHttpRequest, version: int):
    if int(version) == 1 or not version:
        return data_v1()
    raise Http404()

    