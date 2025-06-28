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


from .translateable import Translateable, TranslateableField, TranslateableFieldRecord, TRANSLATIONS
from .http import WebHttpRequest
from .session import Session, get_session_result_id, SessionMeta
from .widget import Widget
from .sessionversion import SessionVersion, SessionVersionWidget
from .choosable import Choosable, ChoosableMeta
from .facette import Facette, FacetteAssignment, FacetteBehaviour, FacetteSelection
from .page import Page, PageMarking
from .facetteselectionwidget import FacetteSelectionWidget
from .facetteradioselectionwidget import FacetteRadioSelectionWidget
from .feedback import Feedback, LanguageFeedback, LanguageFeedbackVote, AssignmentFeedback

from .htmlwidget import HTMLWidget

from .navigationwidget import NavigationWidget
from .resultsharewidget import ResultShareWidget
from .resultlistwidget import ResultListWidget

from .metafilterwidget import MetaFilterWidget,  MetaFilterWidgetStructure, MetaFilterWidgetElement, MetaFilterValue

from .feedbackwidget import FeedbackWidget, GivenFeedback