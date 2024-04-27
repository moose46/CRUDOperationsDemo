from typing import Any, Mapping

from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import Select, TextInput, modelform_factory
from django.forms.utils import ErrorList

from PayRollApp.models import Employee, PartTimeEmployee


# Creating a Form based Model
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"
        widgets = {
            "BirthDate": forms.widgets.DateInput(attrs={"type": "date"}),
            "HireDate": forms.widgets.DateInput(attrs={"type": "date"}),
        }


PartTimeEmployeeForm = modelform_factory(
    PartTimeEmployee, fields=["FirstName", "LastName", "TitleName"]
)


class DynamicPartTimeEmployeeForm(PartTimeEmployeeForm):
    def __init__(self, *args, **kwargs) -> None:
        super(DynamicPartTimeEmployeeForm).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.pop("required", None)
