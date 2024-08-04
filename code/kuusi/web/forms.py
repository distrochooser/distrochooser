from typing import Any, Mapping, Optional, Type, Union
from django.core.exceptions import ValidationError as ValidationError
from django.forms import Form, TextInput
from django.forms.utils import ErrorList
from web.models.facette import FacetteBehaviour

class WarningForm(Form):
    def __init__(self, data: Mapping[str, Any] | None = None) -> None:
        super().__init__(data)
        self.behaviour_warnings = {}
        self.behaviour_information = {}
        self.behaviour_errors = {}
    def add(self, field: str, error: str, criticality: FacetteBehaviour.Criticality):
        target = None
        if criticality == FacetteBehaviour.Criticality.ERROR:
            target = self.behaviour_errors
        elif criticality == FacetteBehaviour.Criticality.WARNING:
            target = self.behaviour_warnings
        else:
            target = self.behaviour_information
        
        if field in target:
            target[field] += f", {error}"
        else:
            target[field] = error

    def add_behaviour_warning(self, field: str, error: str) -> None:
        if field in self.behaviour_warnings:
            self.behaviour_warnings[field] += f", {error}"
        else:
            self.behaviour_warnings[field] = error
    def has_behaviour_warning(self) -> bool:
        return self.behaviour_warnings.keys().__len__() > 0
    def add_behaviour_information(self, field: str, error: str) -> None:
        self.behaviour_information[field] = error
    def has_behaviour_information(self) -> bool:
        return self.behaviour_information.keys().__len__() > 0
    def add_behaviour_error(self, field: str, error: str) -> None:
        self.behaviour_errors[field] = error
    def has_behaviour_error(self) -> bool:
        return self.behaviour_errors.keys().__len__() > 0
    def has_any_behaviour(self) -> bool:
        return self.has_behaviour_error() or self.has_behaviour_information() or self.has_behaviour_warning()