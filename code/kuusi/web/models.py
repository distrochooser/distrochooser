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

from __future__ import annotations
from typing import Any, List
from os.path import join, exists
from os import mkdir, listdir
from logging import getLogger

from django import forms
from django.db import models
from django.db.models import Max, Min
from django.template import loader

from django.http import HttpRequest, HttpResponseRedirect

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.forms import Form, BooleanField

from django.db import models
from django.utils.translation import gettext as _

from polib import pofile

from kuusi.settings import LOCALE_PATHS, LANGUAGES, BASE_DIR

logger = getLogger('root')

class TranslateableField(models.CharField):
    "A field which can be translated"

    def __init__(self, *args, **kwargs):
        kwargs["help_text"] = "A comment for translators to identify this value"
        super().__init__(*args, **kwargs)

    def get_msg_id(self, model_instance: Translateable):
        """
        Get a unique identifier to be used for translation purposes.
        """
        model_type = type(model_instance).__name__
        identifier = model_instance.pk
        if model_instance.catalogue_id:
            identifier = model_instance.catalogue_id
        return f"{model_type}_{identifier}_{self.name}".upper()

    def get_po_block(self, model_instance: Translateable):
        """
        Return the block to be written into the PO file.
        A msg_str might be appended if an translation is existing within the locale context.
        """
        comment = self.value_from_object(model_instance)
        name = self.name
        model_type = type(model_instance).__name__
        pk = model_instance.pk
        msg_id = self.get_msg_id(model_instance)
        return f"\n# Model reference: {model_type}.{pk}\n# Attribute name: {name}, remark: {comment}\nmsgid \"{msg_id}\""

    def pre_save(self, model_instance: Translateable, add: bool) -> Any:
        """
        Update records to make sure there is a record existing at all the time
        """
        if len(LOCALE_PATHS) == 0:
            raise Exception(f"No locale paths are set")
        
        # Make sure that the TranslateAbleField has a record we can reference
        TranslateableFieldRecord.objects.filter(msg_id=self.get_msg_id(model_instance)).delete()
        record = TranslateableFieldRecord.objects.create(
            msg_id = self.get_msg_id(model_instance),
            po_block = self.get_po_block(model_instance)
        )

        logger.debug(f"TranslatableFieldRecord is {record}")
        model_instance.update_po_file()   
        return super().pre_save(model_instance, add)

class TranslateableFieldRecord(models.Model):
    msg_id = models.CharField(null=False, blank=False, max_length=50)
    po_block = models.TextField(null=True, blank=True, max_length=1000)
    def __str__(self) -> str:
        return self.msg_id

class Translateable(models.Model):
    """
    This class is just used to trigger a signal, which clears up unused TranslateableFieldRecords

    If a TranslateField shall be used, the model must inherit this class.
    """
    catalogue_id = models.CharField(null=True, blank=True, default=None, max_length=20) 

    def __(self, key: str, language_code: str = "en") -> str:
        msg_id = self._meta.get_field(key).get_msg_id(self)
        # TODO: make this block in a function
        # TODO: make this in memory
        translation_path = join(LOCALE_PATHS[0], language_code, "LC_MESSAGES", "translateable.po")
        existing_record_translations = {}
        if exists(translation_path):
            po = pofile(translation_path)
            for entry in po:
                existing_record_translations[entry.msgid] = entry.msgstr
        if msg_id not in existing_record_translations or len(existing_record_translations[msg_id]) == 0:
            return msg_id
        return existing_record_translations[msg_id]

    def remove_translation_records(self):
        """ 
        Removes the translation records form the database.
        """
        fields = self._meta.get_fields()

        field: models.Field | TranslateableField
        for field in fields:
            field_type = type(field)
            field_name = field.name
            if isinstance(field, TranslateableField):
                logger.debug(f"Removing field records for {field_type} ({field_name})")
                TranslateableFieldRecord.objects.filter(msg_id = field.get_msg_id(self)).delete()


    def update_po_file(self):
        """
        Update the PO file to represent the currently used records
        """
        for lang in LANGUAGES:
            key = lang[0]
            if not exists(join(LOCALE_PATHS[0], key)):
                mkdir(join(LOCALE_PATHS[0], key))
            if not exists(join(LOCALE_PATHS[0], key, "LC_MESSAGES")):
                mkdir(join(LOCALE_PATHS[0], key, "LC_MESSAGES"))

            translation_path = join(LOCALE_PATHS[0], key, "LC_MESSAGES", "translateable.po")
            existing_record_translations = {}
            if exists(translation_path):
                po = pofile(translation_path)
                for entry in po:
                    existing_record_translations[entry.msgid] = entry.msgstr

            # write the PO file
            all_records = TranslateableFieldRecord.objects.all().order_by("-msg_id")
            with open(translation_path, "w") as file:
                record: TranslateableFieldRecord
                for record in all_records:
                    msg_str = ""
                    if record.msg_id in existing_record_translations:
                        msg_str = existing_record_translations[record.msg_id]
                    file.write(record.po_block + f"\nmsgstr \"{msg_str}\"")

@receiver(pre_delete, sender=Translateable)
def translateable_removing(sender, instance, using, **kwargs):
    origin: Translateable | models.QuerySet = kwargs["origin"]
    if isinstance(origin, models.QuerySet):
        entry: Translateable
        for entry in origin:
            entry.remove_translation_records()
            entry.update_po_file()
    else:
        origin.remove_translation_records()
        origin.update_po_file()


class Page(Translateable):
    title = TranslateableField(null=False, blank=False, max_length=120)
    next_page = models.ForeignKey(to="Page", on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="page_next")
    
    def __str__(self) -> str:
        return f"{self.title}"
    
    @property
    def previous_page(self) -> Page | None:
        return Page.objects.filter(next_page=self).first()

    @property
    def structure(self) -> List[List[Widget]]:
        """
        Returns the structure of the page as a 2-dimensional list containing widgets.

        X and Y are hereby the cols to be used.
        """
        result = list()
        # TODO: add all widget types into this query.
        widgets_used = list(HTMLWidget.objects.filter(pages__pk__in=[self])) + list(NavigationWidget.objects.filter(pages__pk__in=[self]))+ list(FacetteSelectionWidget.objects.filter(pages__pk__in=[self]))

        all_widgets = Widget.objects.filter(pages__in=[self])
        max_row = all_widgets.aggregate(Max('row'))["row__max"]
        max_col = all_widgets.aggregate(Max('col'))["col__max"]
        min_row = all_widgets.aggregate(Min('row'))["row__min"]
        min_col = all_widgets.aggregate(Min('col'))["col__min"]
        if not max_row or not max_col:
            logger.debug(f"The page {self} has no widgets")
            return result
        logger.debug(f"The page {self} spans as follows {min_col},{min_row} -> {max_col}, {max_row}")
        for y in range(min_row, max_row + 1):
            row_list = list()
            for x in range(min_col, max_col + 1):
                matches  = list(filter(lambda w: w.col == x and w.row == y, widgets_used))
                widget = matches[0] if len(matches) > 0 else None
                if widget:
                    row_list.append(widget)
                else:
                    row_list.append(None)
            result.append(row_list)
        return result
    
class Widget(models.Model):
    row = models.IntegerField(default=1, null=False, blank=False)
    col = models.IntegerField(default=1, null=False, blank=False)
    width = models.IntegerField(default=1, null=False, blank=False)
    pages = models.ManyToManyField(to=Page,blank=True,default=None)
    def render(self, request: HttpRequest, page: Page):
        raise Exception()

class HTMLWidget(Widget):
    template = models.CharField(null=False, blank=False, max_length=25)
    def __init__(self, *args, **kwargs):
        template_path = join(BASE_DIR, "web", "templates", "widgets")
        raw_templates = listdir(template_path)
        templates = []
        for template in raw_templates:
            templates.append((template, template))
        self._meta.get_field('template').choices = templates
        self._meta.get_field('template').widget = forms.Select(choices=templates)
        super(HTMLWidget, self).__init__(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.template
    
    def render(self, request: HttpRequest, page: Page):
        render_template = loader.get_template(f"widgets/{self.template}")
        return render_template.render({}, request)

class FacetteSelectionWidget(Widget):
    topic = models.CharField(null=False, blank=False, max_length=120)
    def render(self,request: HttpRequest,  page: Page):
        facettes = Facette.objects.filter(topic=self.topic)
        render_template = loader.get_template(f"widgets/facette.html")
        data = {}
        if request.method == "POST":
            data = request.POST
            # TODO: Read data from database
            # TODO: Show validations warnings
            # TODO: save data

        facette_form = Form(data)
        child_facettes = []
        context = {}


        for facette in facettes:
            is_child = Facette.objects.filter(child_facettes__pk__in=[facette.pk]).count() > 0
            has_child = facette.child_facettes.count() > 0
            if not is_child:
                facette_form.fields[facette.catalogue_id] = BooleanField(required=False)
                if has_child:
                    facette_form.fields[facette.catalogue_id].widget.attrs['data-bs-toggle'] = 'collapse'
                    facette_form.fields[facette.catalogue_id].widget.attrs['data-bs-target'] = f'#collapse-{facette.catalogue_id}'
                    facette_form.fields[facette.catalogue_id].widget.attrs['aria-expanded'] = 'false'
                    facette_form.fields[facette.catalogue_id].widget.attrs['aria-controls'] = f'collapse-{facette.catalogue_id}'

            for sub_facette in facette.child_facettes.all():
                facette_form.fields[sub_facette.catalogue_id] = BooleanField(required=False)
                child_facettes.append(sub_facette.catalogue_id)
        
        context["form"] = facette_form

        return render_template.render({
            "form": facette_form,
            "child_facettes": child_facettes
        }, request)
    
class NavigationWidget(Widget):
    def render(self, request: HttpRequest, page: Page):
        render_template = loader.get_template(f"widgets/navigation.html")
        return render_template.render({
            "page": page
        }, request)
    
class Choosable(Translateable):
    """
    Element ot be choosed. 

    Must be translated
    """
    name = TranslateableField(null=False, blank=False, max_length=120)

    def __str__(self) -> str:
        return f"{self.name}"
    
class Facette(Translateable):
    """
    A facette describes a fact narrowing down the selection for choosables.

    The description will be used for displaying results

    The selectable_description is displayed for selection within a page

    The topic reduces a facette to a certain subarea, e. g. "licenses" for Linux distributions
    """
    description = TranslateableField(null=False, blank=False, max_length=120)
    selectable_description = TranslateableField(null=False, blank=False, max_length=120)
    topic = TranslateableField(null=False, blank=False, max_length=120)
    child_facettes = models.ManyToManyField(to="Facette",blank=True)