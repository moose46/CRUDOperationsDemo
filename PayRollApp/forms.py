from typing import Any, Mapping

from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import Select, TextInput, modelform_factory
from django.forms.utils import ErrorList

from PayRollApp.models import Employee, OnSiteEmployees, PartTimeEmployee


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


# Form Model
class DynamicPartTimeEmployeeForm(PartTimeEmployeeForm):
    def __init__(self, *args, **kwargs) -> None:
        super(DynamicPartTimeEmployeeForm).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.pop("required", None)


class NewPartTimeEmployeeForm(forms.ModelForm):
    class Meta:
        model = PartTimeEmployee
        fields = "__all__"


PartTimeEmployeeFormSet = forms.modelformset_factory(
    PartTimeEmployee, form=NewPartTimeEmployeeForm, extra=10
)


# Form Model
class OnSiteEmployeesForm(forms.ModelForm):
    class Meta:
        model = OnSiteEmployees
        fields = ["first_name", "last_name", "country", "state", "city"]

        widgets = {
            "first_name": TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 300px;",
                    "placeholder": "First Name",
                }
            ),
            "last_name": TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 300px;",
                    "placeholder": "Last Name",
                }
            ),
            "country": Select(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 300px;",
                    "placeholder": "Country",
                }
            ),
            "state": Select(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 300px;",
                    "placeholder": "State",
                }
            ),
            "city": Select(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 300px;",
                    "placeholder": "City",
                }
            ),
        }
