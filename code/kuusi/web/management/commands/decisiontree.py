"""
kuusi
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

from web.models import Session, Feedback, FacetteAssignment

from django.core.management.base import BaseCommand
from logging import getLogger, ERROR

logger = getLogger('command')

class Command(BaseCommand):
    help = "Imports a given *.ku file"
    def handle(self, *args, **options):
        

        # Select the sessions with actual feedback
        sessions = Session.objects.all()
        selected_sessions = []
        session: Session
        assignments = FacetteAssignment.objects.all()
        for session in sessions:
            feedback_count = Feedback.objects.filter(session=session).count() 

            if feedback_count > 0:
                selected_sessions.append(session)

                assignment: FacetteAssignment
                for assignment in assignments:
                    assignment_type = str(assignment.assignment_type)
                    print(assignment_type)

