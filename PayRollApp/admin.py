from django.contrib import admin

from PayRollApp.models import City, Country, Employee, OnSiteEmployees, State

# Register your models here.

admin.site.register(Employee)
admin.site.register(OnSiteEmployees)
admin.site.register(State)
admin.site.register(Country)
admin.site.register(City)
