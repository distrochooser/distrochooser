"""
kuusi
Copyright (C) 2015-2023  Christoph Müller <mail@chmr.eu>

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
from typing import Dict, Tuple, List
from re import match, MULTILINE, finditer, sub, search
from logging import getLogger
from os.path import join, exists, dirname

from django.core.management.base import BaseCommand

from web.models import Facette, Category, FacetteAssignment, Choosable, ChoosableMeta, FacetteBehaviour, random_str, FacetteSelection, Page, SessionVersion, SessionVersionWidget, ResultShareWidget, ResultListWidget, NavigationWidget, FacetteSelectionWidget, HTMLWidget, Session

logger = getLogger("root")


class Command(BaseCommand):
    help = "Imports a given *.ku file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        # FIXME: Implement a better way of handling old, data, e. g. of making the selections orphans, but keep old results.
        # FIXME: Make sure the translatable process omits invalidated entries
        if not options["file_path"]:
            raise Exception("no filename")
        file_path = options["file_path"]
        invalidation_id = random_str()
        
        # Make sure that sessions always keep their "old" invalidation to avoid breaking old results.
        sessions = Session.objects.filter(valid_for="latest")
        session: Session
        for session in sessions:
            session.valid_for = invalidation_id
            session.save()

        with open(file_path, "r") as file:
            raw = file.read()


            includes_re = r"\@include\s+(?P<filename>[^;]+);"
            includes = finditer(includes_re, raw, MULTILINE)

            current_folder = dirname(file_path)
            
            for include in includes:
                line = include.group(0)
                path = include.group("filename")
                final_path = None
                if exists(path):
                    final_path = path
                path = join(current_folder, path)
                if exists(path):
                    final_path = path
                with open(final_path, "r") as include_file:
                    raw = raw.replace(line, include_file.read())


            no_comment_raw = ""
            for line in raw.split("\n"):
                line = line.strip()
                old_line = line
                line = sub(".*\#.+$", "",line)
                if len(line) > 0:
                    no_comment_raw += line + "\n"

            
            lines = no_comment_raw.split(";")

            data_types = {
                "version": self.version,
                "page": self.page,
                "category": self.category,
                "widget": self.widget,
                "facettes": self.facette,
                "behaviour": self.behaviour,
                "assignment": self.assignment,
                "choosable": self.choosable
            }

            results = {}

            data_store = {
                "version": self.version_store,
                "page": self.page_store,
                "category": self.category_store,
                "widget": self.widget_store,
                "facettes": self.facette_store,
                "choosable": self.choosable_store,
                "assignment": self.assignment_store,
                "behaviour": self.behaviour_store
            }

            for key, value in data_types.items():
                results[key] = []
                line: str
                for line in lines:
                    line = line.strip()
                    got = value(line)
                    if got:
                        results[key].append(got)
            for key, value in data_store.items():
                value(invalidation_id, results[key])
    
    def facette_store(self, invalidation_id: str, raw: List[Dict]):
        Facette.objects.filter(is_invalidated=False).update(
            is_invalidated = True,
            invalidation_id = invalidation_id
        )
        for element in raw:
            facette = Facette(
                catalogue_id=f"{element['name']}",
                description=f"{element['name']}-description",
                selectable_description=f"{element['name']}-selectable-description",
                topic=f"{element['topic']}"
            )
            facette.save()

        for element in raw:
            parent = element["parent"]
            if parent:
                child = Facette.objects.get(catalogue_id=element['name'],is_invalidated=False)
                parent = Facette.objects.get(catalogue_id=element['parent'],is_invalidated=False)
                parent.child_facettes.add(child)
                parent.save()

    def choosable_store(self, invalidation_id: str, raw: List[Dict]):
        Choosable.objects.filter(is_invalidated=False).update(
            is_invalidated = True,
            invalidation_id = invalidation_id
        )
        for element in raw:
            choosable = Choosable(
                catalogue_id=f"{element['name']}",
                name=f"{element['name']}",
                description=f"{element['name']}-description",
            )
            choosable.save()
            for meta in element["meta"]:
                meta_type = meta["type"]
                # FIXME: Properly decide between title and name in the ChoosableMeta class.
                meta_title= meta["title"]
                meta_content = meta["content"]
                choosable_meta = ChoosableMeta(
                    meta_choosable = choosable,
                    catalogue_id = f"{element['name']}-{meta_title}",
                    meta_type = meta_type.upper(),
                    meta_title = meta_title,
                    meta_value = meta_content
                )
                choosable_meta.save()

    def assignment_store(self, invalidation_id: str, raw: List[Dict]):
        FacetteAssignment.objects.filter(is_invalidated=False).update(
            is_invalidated = True,
            invalidation_id = invalidation_id
        )
        for element in raw:
            assignment = FacetteAssignment(
                catalogue_id=element["name"],
                description=f"{element['name']}-description",
                long_description=f"{element['name']}-long-description",
                assignment_type=element["weight"].upper()
            )
            assignment.save()
            for facette in element["facettes"]:
                assignment.facettes.add(Facette.objects.get(catalogue_id=facette,is_invalidated=False))
            for target in element["targets"]:
                assignment.choosables.add(Choosable.objects.get(catalogue_id=target,is_invalidated=False))
            assignment.save()

    def behaviour_store(self, invalidation_id: str, raw: List[Dict]): 
        FacetteBehaviour.objects.filter(is_invalidated=False).update(
            is_invalidated = True,
            invalidation_id = invalidation_id
        )
        for element in raw:
            behaviour = FacetteBehaviour(
                catalogue_id=element["name"],
                description=f"{element['name']}-description",
                criticality =element["criticality"].upper(),
                direction =element["direction"].upper()
            )
            behaviour.save()
            for facette in element["subject"]:
                behaviour.affected_subjects.add(Facette.objects.get(catalogue_id=facette,is_invalidated=False))
            for facette in element["object"]:
                behaviour.affected_objects.add(Facette.objects.get(catalogue_id=facette,is_invalidated=False))
            behaviour.save()

    def version_store(self, invalidation_id: str, raw: List[Dict]): 
        SessionVersion.objects.filter(is_invalidated=False).update(
            is_invalidated = True,
            invalidation_id = invalidation_id
        )
        for element in raw:
            version = SessionVersion(
                catalogue_id = element["name"],
                version_name = element["name"]
            )
            version.save()

    def page_store(self, invalidation_id: str, raw: List[Dict]): 
        Page.objects.filter(is_invalidated=False).update(
            is_invalidated = True,
            invalidation_id = invalidation_id
        )
        for element in raw:
            page = Page(
                catalogue_id = element["name"],
                title = element["name"],
                no_header=element["no-header"],
                can_be_marked=element["markable"],
                require_session=element["session"]
            )
            page.save()
            for key in element["not"]:
                page.not_in_versions.add(
                    SessionVersion.objects.get(catalogue_id=key, is_invalidated=False)
                )
            page.save()

        valid_pages = Page.objects.filter(is_invalidated=False)

        page: Page
        for page in valid_pages:
            for element in raw:
                if element["name"] == page.catalogue_id:
                    next_page = element["next"]
                    if next_page:
                        page.next_page = valid_pages.get(catalogue_id=next_page)
                        page.save()

    def category_store(self, invalidation_id: str, raw: List[Dict]): 
        Category.objects.filter(is_invalidated=False).update(
            is_invalidated = True,
            invalidation_id = invalidation_id
        )
        for element in raw:
            page = Category(
                catalogue_id = element["name"],
                name = element["name"],
                target_page=Page.objects.get(catalogue_id=element["to"], is_invalidated=False)
            )
            page.save()
        
        for category in Category.objects.filter(is_invalidated=False):
            for element in raw:
                if element["name"] == category.catalogue_id:
                    if element["parent"]:
                        category.child_of = Category.objects.get(catalogue_id=element["parent"], is_invalidated=False)
                        category.save()

    def widget_store(self, invalidation_id: str, raw: List[Dict]):
        
        class_map = {
            "version": SessionVersionWidget,
            "share": ResultShareWidget,
            "result": ResultListWidget,
            "navigation": NavigationWidget,
            "selection": FacetteSelectionWidget,
            "html": HTMLWidget
        }

        for element in raw:
            if element["type"] in class_map.keys():
                # Widgets won't be invalidated as the pages are invalidated already.
                class_name = class_map[element["type"]]
                new_widget = class_name(
                    row = element["row"],
                    col = element["col"],
                    width = element["width"]
                )
                new_widget.save()
                for page in element["to"]:
                    new_widget.pages.add(Page.objects.get(catalogue_id=page, is_invalidated=False))

                if element["type"] == "selection": 
                    new_widget.topic = element["topic"]

                if element["type"] == "html": 
                    new_widget.template = element["template"]

                new_widget.save()

    def get_name(self, prefix: str, line: str) -> Dict:
        name_text_re = r"@" + prefix + "\s+(?P<name>[\w-]+)"
        matches = match(name_text_re, line)
        if not matches:
            logger.debug(f'Even as "{line}"  failed to parse with prefix {prefix}.')
            return None
        result = {
            "name": matches.group("name"),
        }
        return result

    def get_direction_and_criticality(self, line: str) -> Tuple[str, str]:
        results = {"criticality": "info", "direction": "bidirectional"}
        patterns = {
            "criticality": r".*(?P<value>(warning|info|error)).*",
            "direction": r".*(?P<value>(subject_to_object|object_to_subject|bidirectional)).*",
        }
        for key, pattern in patterns.items():
            matches = match(pattern, line, MULTILINE)
            if matches:
                results[key] = matches.group("value")
        return results["direction"], results["criticality"]

    def facette(self, line: str) -> Dict:
        if "@facette" not in line:
            return None
        else:
            result = self.get_name("facette", line)
            result["parent"] = None
            properties_line = match(r".*\((?P<properties>[^\)]+).*", line)
            if properties_line:
                properties_line_content = properties_line.groupdict()["properties"]
                topic_re = r"topic\s(?P<topic>[\w-]+)"
                topic_match = match(topic_re, properties_line_content)
                if topic_match:
                    result["topic"] = topic_match.group("topic")
                else:
                    logger.debug(
                        f"The facette {result['name']} does not feature a topic."
                    )
            else:
                logger.debug(
                    f"The facette {result['name']} does not feature any properties."
                )

            parent_re = r".*parent\s+(?P<target>[\w-]+)"
            parent = match(parent_re, line)

            if parent:
                result["parent"] = parent.group("target")
            return result

    def behaviour(self, line: str) -> Dict:
        if "@behaviour" not in line:
            return None
        else:
            result = self.get_name("behaviour", line)

            relation_line = match(r".*\((?P<relations>[^\)]+).*", line)
            if relation_line:
                relation_line_contents = relation_line.groupdict()["relations"]
                target_re = r"(?P<what>(subject|object))\s{1,}(?P<target>[\w-]+)"
                matches = finditer(target_re, relation_line_contents)
                result["subject"] = []
                result["object"] = []
                if matches:
                    for relation_match in matches:
                        groups = relation_match.groupdict()
                        what = groups["what"]
                        target = groups["target"]
                        result[what].append(target)

            direction, criticality = self.get_direction_and_criticality(line)
            result["direction"] = direction
            result["criticality"] = criticality
            return result

    def assignment(self, line: str) -> Dict:
        if "@assignment" not in line:
            return None
        else:
            result = self.get_name("assignment", line)
            relation_line = match(r".*\((?P<relations>[^\)]+).*", line)
            result["facettes"] = []
            result["weight"] = "positive"
            result["targets"] = []
            if relation_line:
                relation_line_contents = relation_line.groupdict()["relations"]
                haystack = relation_line_contents.split(" ")

                for needle in haystack:
                    result["facettes"].append(needle.strip())
            weight_re = r".*(?P<value>(positive|negative|neutral)).*"
            weight = match(weight_re, line)
            if weight:
                result["weight"] = weight.group("value")

            target_re = r"to\s+(?P<target>[\w-]+)"
            targets = finditer(target_re, line, MULTILINE)
            for target in targets:
                result["targets"].append(target.group("target"))

            return result

    def choosable(self, line: str) -> Dict:
        if "@choosable" not in line:
            return None
        else:
            result = self.get_name("choosable", line)

            properties_line = match(r".*\((?P<properties>[^\)]+).*", line)
            if properties_line:
                properties_line_contents = properties_line.groupdict()["properties"]
                target_re = r"(?P<what>(link|flag|text|date))\s{1,}(?P<title>[\w-]+)\s{1,}(?P<content>[\w-]+)"
                matches = finditer(target_re, properties_line_contents)
                result["meta"] = []
                if matches:
                    for property_match in matches:
                        groups = property_match.groupdict()
                        what = groups["what"]
                        title = groups["title"]
                        content = groups["content"]
                        result["meta"].append({"type": what,"title": title, "content": content})
            return result

    def version(self, line: str) -> Dict:
        if "@version" not in line:
            return None
        else:
            result = self.get_name("version", line)
            return result

    def page(self, line: str) -> Dict:
        if "@page" not in line:
            return None
        else:
            result = self.get_name("page", line)
            result["not"] = []
            result["next"] = None
            properties_line = match(r".*\((?P<properties>[^\)]+).*", line)
            if properties_line:
                properties_line_contents = properties_line.groupdict()["properties"]
                needles = [
                    "session",
                    "markable",
                    "no-header"
                ]
                for needle in needles:
                    result[needle] = needle in properties_line_contents
            pattern = r".*not\s+(?P<name>[\w-]+)"
            matches = finditer(pattern, line)
            for name_match in matches:
                name = name_match.group("name")
                result["not"].append(name)

            pattern = r".*next\s+(?P<name>[\w-]+)"
            name_match = match(pattern, line)
            if name_match:
                name = name_match.group("name")
                result["next"] = name
            return result
        
    def category(self, line: str) -> Dict:
        if "@category" not in line:
            return None
        else:
            result = self.get_name("category", line)  
            result["to"] = None
            result["parent"] = None
            properties_line = match(r".*\((?P<properties>[^\)]+).*", line)
            if properties_line:
                properties_line_contents = properties_line.groupdict()["properties"]
                result["icon"] = properties_line_contents
            
            pattern = r"to\s+(?P<name>[\w-]+)"
            matches = search(pattern, line)
            if matches:
                name = matches.group("name")
                result["to"] = name
            pattern = r"parent\s+(?P<name>[\w-]+)"
            matches = search(pattern, line)
            if matches:
                name = matches.group("name")
                result["parent"] = name
            return result

    def widget(self, line: str) -> Dict:
        if "@widget" not in line:
            return None
        else:
            result = self.get_name("widget", line)
            result["type"] = result["name"]
            result["to"] = []
            result.update(self.coords(line))

            pattern = r"to\s+(?P<name>[\w-]+)"
            matches = finditer(pattern, line)
            for name_match in matches:
                name = name_match.group("name")
                result["to"].append(name)
        
            pattern = r".*topic\s+(?P<topic>[\w-]+)"
            topic_match = match(pattern, line)
            if topic_match:
                name = topic_match.group("topic")
                result["topic"] = name
            widget_types = {
                "html": self.htmlwidget,
                "selection": self.selectionwidget
            }
            for key, value in widget_types.items():
                if result["type"] == key:
                    result.update(value(line))
            return result
        
    def coords(self, line: str) -> Dict:
        pattern = ".*(?P<row>[\d]+)\s+(?P<col>[\d]+)\s+(?P<width>[\d]+).*"
        results = match(pattern, line)

        data = {}
        if results:
            data["row"] = results.group("row")
            data["col"] = results.group("col")
            data["width"] = results.group("width")
            return data
        else:
            return None
        
    def htmlwidget(self, line: str) -> Dict:
        pattern = "(?P<template>[\w-]{1,}\.html)"
        results = search(pattern, line) 

        if results:
            return {
                "template": results.group("template")
            }
        return None   
    
    def selectionwidget(self, line: str) -> Dict:
        pattern = "(?P<topic>[\w-]{1,})\s{0,}$"
        results = search(pattern, line) 

        # TODO: Decide to use .description or not.

        if results:
            return {
                "topic": results.group("topic")
            }
        return None