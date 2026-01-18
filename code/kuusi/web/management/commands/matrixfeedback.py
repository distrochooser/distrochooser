"""
distrochooser
Copyright (C) 2014-2026 Christoph Müller <mail@chmr.eu>

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

from genericpath import exists
from json import dumps, loads
from os import listdir
from web.models import Feedback
from django.core.management.base import BaseCommand
from logging import getLogger, ERROR
from os.path import join
from kuusi.settings import LOCALE_PATHS

logger = getLogger("command")


class Command(BaseCommand):
    help = "Review provided mapping feedback"

    def add_arguments(self, parser):
        parser.add_argument("--delete", type=int, nargs="*")
        parser.add_argument("--approve", type=int, nargs="*")

    def handle(self, *args, **options):
        to_delete = options["delete"]
        to_approve = options["approve"]

        if to_delete is not None:
            for pk in to_delete:
                feedback = Feedback.objects.get(pk=pk)
                Feedback.objects.filter(choosable=feedback.choosable).filter(assignment=feedback.assignment).filter(is_positive=feedback.is_positive).delete()
        if to_approve is not None:
            for pk in to_approve:
               feedback = Feedback.objects.get(pk=pk)
               assignment = feedback.assignment
               if not feedback.is_pending:
                    raise Exception("There is nothing to do. Element is not pending")
               assignment.choosables.add(feedback.choosable)
               feedback.delete()
               assignment.save()
               
        # The data contains duplicates
        data = Feedback.objects.all().order_by( "assignment", "choosable", "is_positive")
        ignore_duplicate_list = []
        for element in data:

            ignore_needle = f"{element.choosable.pk}_{element.assignment.pk}_{element.is_positive}"
            if ignore_needle not in ignore_duplicate_list:
                votes = element.assignment.get_votes()
                matching_votes = list(filter(lambda l: l[0] == element.choosable.pk, votes))[0]
                positive_votes = matching_votes[1]
                negative_votes = matching_votes[2]
                pending_string = "NEW" if element.is_pending else "FEEDBACK"
                positive_string = "POSITIVE" if element.is_positive else "NEGATIVE"
                duplicates = data.exclude(pk=element.pk).filter(choosable=element.choosable).filter(assignment=element.assignment).filter(is_positive=element.is_positive)

                print(
                    f"[{element.pk}] {positive_string}, {pending_string} {element.choosable}[+{positive_votes}/-{negative_votes}] => " + element.assignment.__("description")  + f" ({duplicates.count()}) duplicates"
                )
                ignore_duplicate_list.append(ignore_needle)



