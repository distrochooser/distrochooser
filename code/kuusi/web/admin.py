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

from django.contrib import admin

from web.models import Choosable,Feedback, MetaFilterWidget, TranslateableFieldRecord, Translateable, Category, Page, Widget, FacetteRadioSelectionWidget, HTMLWidget, NavigationWidget, FacetteSelectionWidget, Facette, FacetteBehaviour, SessionVersionWidget, Session, SessionMeta, SessionVersion, FacetteSelection, ResultShareWidget, ResultListWidget, FacetteAssignment, PageMarking, ChoosableMeta

[admin.site.register(*models) for models in [
    (Choosable,),
    (ChoosableMeta,),
    (TranslateableFieldRecord,),
    (Translateable,),
    (Category,),
    (Page,),
#    (Widget,), just for debugging (is base class only)
    (HTMLWidget,),
    (NavigationWidget,),
    (FacetteSelectionWidget,),
    (FacetteRadioSelectionWidget,),
    (MetaFilterWidget,),
    (Facette,),
    (FacetteBehaviour,),
    (Session,),
    (SessionMeta,),
    (SessionVersion,),
    (FacetteSelection,),
    (ResultShareWidget,),
    (ResultListWidget,),
    (SessionVersionWidget,),
    (FacetteAssignment,),
    (PageMarking,),
    (Feedback,),
]]