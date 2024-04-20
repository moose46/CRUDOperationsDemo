from django.urls import path

from PayRollApp import views

urlpatterns = [
    path("EmployeesList", views.EmployeesList, name="EmployeesList"),
    path("EmployeeDetails/<int:id>", views.EmployeeDetails, name="EmployeeDetails"),
    path("EmployeeDelete/<int:id>/", views.EmployeeDelete, name="EmployeeDelete"),
]