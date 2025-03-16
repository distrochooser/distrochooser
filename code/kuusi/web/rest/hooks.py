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

from requests import post
from kuusi.settings import DISCORD_HOOK, KUUSI_URL
from web.models import Session
from langcodes import standardize_tag
from unicodedata import lookup
from urllib3.util import parse_url
from threading import Thread

def get_flag_str(lang_code:str) -> str:
    flag_str = ""
    for char in lang_code:
        flag_str += lookup(f'REGIONAL INDICATOR SYMBOL LETTER {char}')
    return flag_str
def fire_hook(content, session: Session,  title: str, color: int):
    if not DISCORD_HOOK:
        return
    if not content or len(content) == 0:
        return
    instance_url = parse_url(KUUSI_URL)

    headers = {"content-type": "application/json"}
    lang_code = standardize_tag(session.language_code, macro=True)
    flag_str = get_flag_str(lang_code)
    
    user_agent = "" if not session.user_agent else session.user_agent
    ref = "" if not session.referrer else f" from: {session.referrer}"
    data = {
        "username": f"[{instance_url.host}] {session.result_id} ({session.language_code}-{flag_str}) {user_agent}{ref}"
    }
    # leave this out if you dont want an embed
    # for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data["embeds"] = [
        {
            "description": content,
            "title": title,
            "color": color,
        }
    ]

    # run into separate thread
    try:
        t = Thread(
            target = post,
            kwargs={
                "url":DISCORD_HOOK,
                "headers":headers,
                "json":data,
            }
        )
        t.start()
    except:
        pass
