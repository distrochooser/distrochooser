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

from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify

from web.models.choosable import ChoosableMeta
from web.models.facette import FacetteAssignment, Facette
from web.templatetags.web_extras import _i18n_

from termcolor import colored
import os

class Command(BaseCommand):
    help = "Imports a given *.ku file"
    def clear(self):
        delegate = lambda: os.system('cls' if os.name=='nt' else 'clear')
        delegate()

    def print_facettes(self, facettes):

        for index, facette in enumerate(facettes):
            cat_id = facette.catalogue_id
            topic = facette.topic
            translate_value = _i18n_("en", f"{cat_id}-selectable_description")["value"]
            
            print(f"[{colored(index, 'blue')}] [{colored(topic, 'yellow')}] {colored(translate_value, 'magenta')}")

    def print_assignment(self, assignment: FacetteAssignment, index, selected_assignments, with_details: bool = False):
        translate_id = assignment.catalogue_id   
        translate_value = _i18n_("en", f"{translate_id}-long_description")["value"]
        assignment_type = assignment.assignment_type
        color_map = {
            FacetteAssignment.AssignmentType.BLOCKING: "white",
            FacetteAssignment.AssignmentType.NEGATIVE: "red",
            FacetteAssignment.AssignmentType.NEUTRAL: "blue",
            FacetteAssignment.AssignmentType.POSITIVE: "green",
        }
        selected_color = color_map[assignment_type]
        selected_string = f"{colored('X', 'red')}" if index in selected_assignments else  ""
        translation_color = "light_yellow" if index in selected_assignments else "light_grey"
        print(f"[{colored(index, 'cyan')}] {colored(assignment_type, selected_color)}: {colored(translate_value, translation_color)} {selected_string}")
        if with_details:
            choosable_str = ""
            for choosable in assignment.choosables.all():
                choosable_str += str(choosable) + ","
            choosable_str = choosable_str.strip(",")
            print(choosable_str)


    def print_assignments(self, assignments, selected_assignments):
        for index, assignment in enumerate(assignments):      
            self.print_assignment(assignment, index, selected_assignments)

    def write(self):
        pass

    def handle(self, *args, **options):
       
            
        

        assignments = FacetteAssignment.objects.all()
        assignment_list = list(assignments)
        facettes = Facette.objects.all()
        selected_assignments = []
        data= {}

        action = "list"
        while action != "exit":
            do_print = True
            if "new" in action or action == "n":
                name = input("Name the for this choosable: ")
                catalogue_id = slugify(name)
                data = {
                    "name": name,
                    "catalogue_id": catalogue_id,
                    "meta": {},
                    "new_assignments": []
                }

            elif "show" in action or "s " in action: 
                do_print = False
                parts = action.split(" ")
                if len(parts) == 2:
                    index = int(parts[1].strip())
                    assignment = assignment_list[index]
                    self.print_assignment(assignment, index, selected_assignments, True)
            if "toggle" in action or "t " in action:
                parts = action.split(" ")
                if len(parts) == 2:
                    raw_numbers = parts[1].strip()
                    indexes = []
                    if "," in raw_numbers:
                        indexes = raw_numbers.split(",")
                    else:
                        index = parts[1].strip()
                        indexes.append(index)
                    for index in indexes:
                        parsed = int(index)
                        selected_assignments.append(parsed) if parsed not in selected_assignments else selected_assignments.remove(parsed)
            elif action == "status" or "s " in action:
                print(f"New choosable: {data['name']} <{colored(data['catalogue_id'], 'light_magenta')}>")
                for assignment_index in selected_assignments:
                    assignment = assignment_list[assignment_index]
                    print(f"Assigning to {colored(assignment, 'light_yellow')}")
                for meta_key, meta_value in data["meta"].items():
                    print(f"{colored(meta_key, 'light_yellow')}: {colored(meta_value, 'cyan')}")
                do_print = False
            elif action == "meta" or "m " in action:

                meta_names = ChoosableMeta.MetaName.choices
                for value in meta_names:
                    meta_name_key = value[0]
                    old_value = "" if meta_name_key not in data["meta"] else f" [{data['meta'][meta_name_key]}]"
                    meta_value = input(f"Add value for meta {meta_name_key}{old_value}? (Empty for no value) ")
                    if meta_value:
                        data["meta"][meta_name_key] = meta_value
                do_print = False
            elif action == "facettes" or action == "f":
                do_print = False
                self.print_facettes(facettes)
            elif action == "create":
                got = input("What text should the new assignment have?")
                slug = slugify(got)
                data["assignments"].append({
                    "text": got,
                    "catalogue_id": slug
                })
            elif action == "write":
                self.write()
            if do_print:
                self.clear()
                self.print_assignments(assignments, selected_assignments)

           
            action = input(f"Action (Show <index>|exit|status|Toggle <index>|New|Meta|Create assignment|list Facettes|write toml): ")
        

        