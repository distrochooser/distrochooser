from typing import Any, Mapping, Optional, Type, Union
from django.core.exceptions import ValidationError as ValidationError
from django.forms import Form
from django.forms.utils import ErrorList

class WarningForm(Form):
    def __init__(self, data: Mapping[str, Any] | None = None) -> None:
        super().__init__(data)
        self.warnings = {}
    def add_warning(self, field: str, error: str) -> None:
        self.warnings[field] = error
    def has_warning(self) -> bool:
        return self.warnings.keys().__len__() > 0