from ast import mod
from tkinter import Widget

from django.db import models
from django.forms import CharField
from pyexpat import model


class Department(models.Model):
    DeptName = models.CharField(max_length=30)
    LocationName = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.DeptName


class Country(models.Model):
    CountryName = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.CountryName


# Create your models here.
class Employee(models.Model):
    COUNTRIES = [
        ("IND", "India"),
        ("USA", "United States of America"),
        ("UK", "United Kingdom"),
        ("AUS", "Australia"),
        ("AU", "Australia"),
        ("SP", "Spain"),
    ]

    FirstName = models.CharField(max_length=30)
    LastName = models.CharField(max_length=30)
    TitleName = models.CharField(max_length=30)
    HasPassport = models.BooleanField()
    Salary = models.IntegerField()
    BirthDate = models.DateField()
    HireDate = models.DateField()
    Notes = models.CharField(max_length=200)
    # Country = models.CharField(max_length=35, choices=COUNTRIES, default=None)
    Email = models.EmailField(default="", max_length=50)
    PhoneNumber = models.CharField(default="", max_length=20)
    EmpDepartment = models.ForeignKey(
        "Department", default=0, on_delete=models.PROTECT, related_name="Departments"
    )
    EmpCountry = models.ForeignKey(
        "Country", default=0, on_delete=models.PROTECT, related_name="Countries"
    )


class PartTimeEmployee(models.Model):
    FirstName = models.CharField(max_length=30)
    LastName = models.CharField(max_length=30)
    TitleName = models.CharField(max_length=30)


class State(models.Model):
    name = models.CharField(max_length=100, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, default=None)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100, null=True)
    state = models.ForeignKey(State, on_delete=models.PROTECT, default=None)

    def __str__(self):
        return self.name


class OnSiteEmployees(models.Model):
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, default=None)
    state = models.ForeignKey(State, on_delete=models.PROTECT, default=None)
    city = models.ForeignKey(City, on_delete=models.PROTECT, default=None)

    def __str__(self) -> str:
        return str(self.first_name)
