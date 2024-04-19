from django.db import models


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
    HasPasport = models.BooleanField()
    Salary = models.IntegerField()
    BirthDate = models.DateField()
    HireDate = models.DateField()
    Notes = models.CharField(max_length=200)
    Country = models.CharField(max_length=35, choices=COUNTRIES, default=None)
    Email = models.EmailField(default="", max_length=50)
    PhoneNumber = models.CharField(default="", max_length=20)
