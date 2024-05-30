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

# convert viisi.json/ xy.po to toml and json files

# This script was done quick and dirty to avoid giving translators a ton of work to do.



from os import listdir
from json import loads, dumps
from polib import pofile

from env import old_translation_paths, facette_file, page_file, matrix_path, locale_path

data = loads(open("./viisi.json").read())



# get distros

raw_distros = list(filter(lambda m: m["model"] == "distrochooser.distribution", data))

choosables = []

for distro in raw_distros:
    choosables.append({
        "catalogue_id": distro["fields"]["identifier"],
        "url": distro["fields"]["url"],
        "pk": distro["pk"],
        "name": distro["fields"]["name"],
        "identifier": distro["fields"]["identifier"].lower(),
        "bg_color": distro["fields"]["bgColor"],
        "fg_color": distro["fields"]["fgColor"],
    })

with open(matrix_path + "choosables.toml", "w+") as file:
    content = ""
    for choosable in choosables:
        content += "[[choosable]]\n"
        content += f"catalogue_id=\"{choosable['identifier']}\"\n"
        content += f"bg_color=\"{choosable['bg_color']}\"\n"
        content += f"fg_color=\"{choosable['fg_color']}\"\n"

        content += "[[choosable.meta]]\n"
        content += "meta_type=\"link\"\n"
        content += "meta_name=\"website\"\n"
        content += f"meta_value=\"{choosable['url']}\"\n"
    file.write(content)


raw_answers= list(filter(lambda m: m["model"] == "distrochooser.answer", data))

answer_map = {
    "software-use-case-anonymous-answer": "privacy-usage",
    "software-use-case-answer-daily": "daily-usage",
    "software-use-case-answer-gaming": "gaming-usage",
    "software-use-case-isolation": "privacy-isolation-usage",
    "software-use-case-blind": "impaired-view-usage",
    "live-mode-only": "live-mode-usage",
    "computer-knowledge-answer-beginner": "beginner-usage",
    "computer-knowledge-answer-advanced": "advanced-usage",
    "computer-knowledge-answer-professional": "professional-usage",
    "linux-knowledge-answer-beginner": "no-linux-contact",
    "linux-knowledge-answer-advanced": "already-used",
    "linux-knowledge-answer-professional": "knowledge-present",
    "presets-question-answer-manypresets": "many-preselections",
    "presets-question-answer-guiselections": "many-choices-gui",
    "presets-question-answer-ownselection": "commandline-setup",
    "hardware-question-oldpc": "no64bit",
    "hardware-question-newpc": "64bit",
    "help-question-tutorials": "manuals",
    "help-question-user-exchange": "need-human-help",
    "price-answer-free": "pricing-free",
    "price-answer-paid": "paid-support-ok",
    "scope-answer-fullinstall": "scope-out-of-the-box",
    "scope-own-selection": "scope-answer-ownselection",
    "ideology-answer-free": "license-open-source",
    "ideology-answer-proprietary-ok": "proprietary-okay-when-working",
    "privacy-answer-highprivacy":"privacy-no-connections-unless-wanted",
    "privacy-answer-services-ok": "okay-when-working",
    "software-admin-answer-appstore": "app-store-gui",
    "software-admin-answer-console": "software-admin-answer-console",
    "answer-avoid-systemd": "no-systemd",
    "software-updates-answer-fast": "prefer-fast",
    "software-updates-answer-slow": "prefer-stable",
    "ux-concept-answer-mac-like": "ux-concept-answer-mac-like",
    "ux-concept-answer-windows-like": "ux-concept-answer-windows-like"
}


answers = []
for answer in raw_answers:
    if answer["fields"]["msgid"] in answer_map:
        answers.append({
            "msgid": answer["fields"]["msgid"],
            "pk": answer["pk"],
            "old_blocked": answer["fields"]["blockedAnswers"],
            "new_msgid": answer_map[answer["fields"]["msgid"]],
        })

for answer in answers:
    answer["blocked"] = list(map(lambda ax: "\"" +ax["new_msgid"]  +"\"", filter(lambda ax: ax["pk"] in answer["old_blocked"], answers)))

raw_answerdistributionmatrix = list(filter(lambda m: m["model"] == "distrochooser.answerdistributionmatrix", data))

ignored_assignments = [
    "matrix-computer-knowledge-higher-facette-advanced-usage",
    "matrix-computer-knowledge-higher-facette-professional-usage"
]

seen_assigments = {}
assignment_content =""
for matrix in raw_answerdistributionmatrix:
    ref_distros = list(map(lambda d: f"\"{d['catalogue_id']}\"",filter(lambda c: c["pk"] in matrix["fields"]["distros"], choosables)))
    ref_facettes = list(map(lambda a: f"\"{a['new_msgid']}\"", filter(lambda a: a["pk"] == matrix["fields"]["answer"], answers)))

    description = matrix["fields"]["description"]
    pk = matrix["pk"]
    for facette in ref_facettes:
        description += "-facette-" +  facette.replace("\"", "")


    is_neutral = matrix["fields"]["isNeutralHit"]
    is_negative = matrix["fields"]["isNegativeHit"]
    is_blocking = matrix["fields"]["isBlockingHit"]
    if len(ref_facettes) == 0:
        print(f"omitting {description} due to emptyness")
    else:
        how_str = "positive"
        candidate = {
            "is_negative": is_negative,
            "is_neutral": is_neutral,
            "is_blocking": is_blocking,
            "description": description,
            "distros": ref_distros,
            "facettes": ref_facettes,
            "old_description": matrix["fields"]["description"]
        }
        if description not in seen_assigments:
        
            if is_neutral:
                how_str = "neutral"


            if is_negative:
                how_str = "negative"

            if is_blocking:
                how_str = "blocking"

            if description not in ignored_assignments:
                assignment_content += f"[assignment.{description}]\n"
                assignment_content += f"long_description = \"{description}\"\n"
                assignment_content += f"from = [{','.join(ref_facettes)}]\n"
                assignment_content += f"to = [{','.join(ref_distros)}]\n"
                assignment_content += f"how = \"{how_str}\"\n"
            else:
                print(f"Ignoring to add {description} to assignment content")
            seen_assigments[description] = candidate


        else:
            reference_candidate = seen_assigments[description]

            print(f"{pk}{description} ALREADY SEEN")



# we assume all distrochooser 5 matrix blocks as bidrectional

assignment_content += "\n"
for answer in answers:
    for key, blocked in enumerate(answer["blocked"]):
        assignment_content += f"[behaviour.{answer['new_msgid']}-{key}]\n"
        assignment_content += "direction=\"BIDIRECTIONAL\"\n"
        assignment_content += f"subjects=[\"{answer['new_msgid']}\"]\n"
        assignment_content += f"objects=[{','.join(answer['blocked'])}]\n"
        assignment_content += "criticality=\"WARNING\"\n"

with open(matrix_path + "assignments.toml", "w+") as file:
    file.write(assignment_content)








# create translations

# create maps for page and facettes on the fly
old_locales = listdir(old_translation_paths)
facette_map = {}
page_map = {}
category_map = {
    "welcome-page-category-name": "category-welcome",
    "scenario-page-category-name": "software-use-case",
    "pc-knowledge-page-category-name": "computer-knowledge-category",
    "linux-knowledge-page-category-name": "linux-knowledge-category",
    "installation-page-category-name": "presets-category",
    "old-hardware-category-name": "hardware-category",
    "help-category-name": "help-category",
    "ux-category-name": "ux-concept-category",
    "pricing-category-name": "price-category",
    "scope-category-name": "scope-category",
    "ideology-category-name": "ideology-category",
    "privacy-category-name": "privacy-category",
    "administration-category-name": "software-admin-category",
    "updates-category-name": "software-updates-category",
    "result-category-name": "recommendation-category"
}

ui_map = {
    "WELCOME_WIDGET_HEADER": "welcome-text-title",
    "WELCOME_WIDGET_TEXT": "welcome-text-skip",
    "WELCOME_WIDGET_SKIP_QUESTIONS": "welcome-text-skip",
    "WELCOME_WIDGET_GET_ANSWER_ANY_TIME": "welcome-text-result-get",
    "WELCOME_WIDGET_ANY_ORDER": "welcome-text-order",
    "WELCOME_WIDGET_DELETE_ANY_TIME": "welcome-text-remove",
    "BTN_NEXT_PAGE": "next-question",
    "BTN_PREV_PAGE": "prev-question",
    "LINK_ABOUT": "about-header",
    "LANGUAGE": "language",
    "ABOUT_PAGE_TITLE": "about",
    "ABOUT_PAGE_TEXT": "about-intro-text",
    "PRIVACY_PAGE_TITLE": "privacy-header"
}

locales = ["en"] + list(map(lambda l: l.replace(".po", ""), filter(lambda l: ".po" in l, old_locales)))

for locale in locales:
    entries_raw = pofile(f"./old-translations/{locale}.po")
    entries = {}
    for entry in entries_raw:
        entries[entry.msgid] = entry.msgstr
    if locale == "en":
        # build the maps for facettes and pages on the fly as I'm stupid
        en_content_facettes = loads(open(facette_file, "r").read())
        for key, value in en_content_facettes.items():
            for old_key, old_value in entries.items():
                if old_value == value:
                    facette_map[old_key] = key

        en_content_pages = loads(open(page_file, "r").read())
        for key, value in en_content_pages.items():
            for old_key, old_value in entries.items():
                if old_value == value:
                    page_map[old_key] = key
    choosable_texts= {}
    for choosable in choosables:
        old_msgid = choosable["identifier"]
        #identifer-description
        description = entries[f"description-{old_msgid}"]
        #identifier-name
        choosable_texts[f"{old_msgid}-name"] = choosable["name"]
        choosable_texts[f"{old_msgid}-description"] = description
    
    with open(locale_path + f"choosable-{locale}.json", "w+") as file:
        file.write(dumps(choosable_texts, indent=4))
    assignment_texts = {}
    for _, assignment in seen_assigments.items():
        if assignment["old_description"] in entries:
            old_translations = entries[assignment["old_description"]]
            assignment_texts[assignment["description"] + "-long_description"] = old_translations
    
    with open(locale_path + f"facetteassignment-{locale}.json", "w+") as file:
        file.write(dumps(assignment_texts, indent=4))
    facette_texts = {}
    for key, value in facette_map.items():
        facette_texts[value] = entries[key]
    with open(locale_path + f"facette-{locale}.json", "w+") as file:
        file.write(dumps(facette_texts, indent=4))
    page_texts = {
        "version-page-text": "You can select a simplified questionaire edition, which removes some super technical questions",
        "linux-knowledge-page-text": "How would you rate your knowledge with the Linux operating system?"
    }
    for key, value in page_map.items():
        page_texts[value] = entries[key]
    with open(locale_path + f"page-{locale}.json", "w+") as file:
        file.write(dumps(page_texts, indent=4))
    category_texts = {
        "version-page-category-name": "Questionaire edition"
    }
    for key, value in category_map.items():
        category_texts[key] = entries[value]
    with open(locale_path + f"category-{locale}.json", "w+") as file:
        file.write(dumps(category_texts, indent=4))
    ui_texts = {}
    for key, value in ui_map.items():
        ui_texts[key] = entries[value]
    
    # New texts required
    ui_texts["WELCOME_MARK_UNSURE"] = "You can highlight questions where you are unsure about your answer"
    ui_texts["WELCOME_WIDGET_MARK_WEIGHT"] = "You can weight answers influence your result"
    ui_texts["COOKIES_ALERT"] = "We use cookies for techical reasons. There won't be any personalized tracking. You can find more information on the following page:"
    ui_texts["LINK_PRIVACY"] = "Our privacy information"
    ui_texts["BTN_RESET_ANSWER"] = "Reset your answers"    
    ui_texts["BTN_MARK"] = "Mark this question"  
    ui_texts["BTN_UNMARK"] = "Unmark this question"
    ui_texts["LINK_IMPRINT"] = "Imprint"
    ui_texts["DEBUG_MODE_ON_DESCRIPTION"] = "The debug mode is ON. Expect additional output."
    ui_texts["LANGUAGE_CHANGE"] = "Change language"
    ui_texts["BOOKMARKED_STEP"] = "Marked"
    ui_texts["FULL_VERSION"] = "Full version"
    ui_texts["WEIGHT_LABEL"] = "Weight"
    ui_texts["YOUR_RESULT_LINK_LABEL"] = "Your result link"
    ui_texts["BLOCKING"] = "Blocking issue"
    ui_texts["NEGATIVE"] = "Not suitable based on your answers"
    ui_texts["NEUTRAL"] = "Neutral property"
    ui_texts["POSITIVE"] = "Positive match"
    ui_texts["website"] = "Distribution homepage"
    ui_texts["created"] = "Date of creation"
    ui_texts["ABOUT_PAGE_TEXT_STATS"] = "Amount of tests created since 14.06.2024:"
    ui_texts["ABOUT_PAGE_LICENSE_TITLE"] = "License"
    ui_texts["ABOUT_PAGE_LICENSE_TEXT"] = "Distrochooser.de is Open Source software. You can find more information about the license on "
    ui_texts["ABOUT_PAGE_LICENSE_LINK"] = "link to our public repository."
    ui_texts["PRIVACY_PAGE_EXTERNAL_LINK"] = "external link"
    ui_texts["ABOUT_PAGE_LICENSE_DATABASE_TEXT"] = "Starting with version 6, the decision matrix is part of the repository. You can find the definition in the /doc/ folder. The live data might be published at a later point."
    ui_texts["PRIVACY_PAGE_TEXT"] = "Distrochooser.de does not utilze any personalized logging. Due to technical reasons, the page sets a cookie as described below."
    ui_texts["PRIVACY_PAGE_COOKIE_TEXT"] = "Following cookies are created:"
    ui_texts["PRIVACY_PAGE_CSRF_COOKIE_SESSION_LIFETIME"] = "To implement a security mechanism called CSRF, the page creates a random session key which is stored in a cookie. This cookie has a long livetime due to technical reasons."
    ui_texts["PRIVACY_PAGE_CSRF_COOKIE_SESSION_LIFETIME_DOCS"] = "You can find more information on this page"
    ui_texts["PRIVACY_PAGE_COOKIE_SESSION_LIFETIME"] = "Sesion data. Is used to remember which answers are selected"
    ui_texts["LOCALE_INCOMPLETE"] = "This translation is incomplete. You can help by providing missing translation values here!"
    ui_texts["PRIVACY_PAGE_STORED_DATA"] = "What data do we store?"
    ui_texts["PRIVACY_PAGE_STORED_TEXT"] = "We do not save personalized data. We store following statistical information about the result:"
    ui_texts["PRIVACY_PAGE_STORED_TEXT_DATE_TIME"] = "Date and time"
    ui_texts["PRIVACY_PAGE_STORED_TEXT_USER_AGENT"] = "Your browser user agent, which does not identify a specific user"
    ui_texts["PRIVACY_PAGE_STORED_REF"] = "A referrer, if any. Your browser settings might already empty this information"
    ui_texts["PRIVACY_PAGE_STORED_TEXT_WHY"] = "We store this information to allow us to create statistics about the usage of the service. The data is generic and is not related to specific users and has the goal to identify issues with the service itself"
    ui_texts["PRIVACY_PAGE_TITLE"] = "Privacy"
    ui_texts["ABOUT_PAGE_TITLE"] = "About this project"
    ui_texts["IMPRINT_TITLE"] = "Imprint"
    ui_texts["IMPRINT_DISCLAIMER_TITLE"] = "Disclaimer"
    ui_texts["IMPRINT_DISCLAIMER_TEXT"] = "We do not take any liability for the pages linked in this service. If you find a malicous link on this website, please inform us using our contact information."
   
    with open(locale_path + f"ui-{locale}.json", "w+") as file:
        file.write(dumps(ui_texts, indent=4))
