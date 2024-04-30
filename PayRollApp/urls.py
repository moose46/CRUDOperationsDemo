from django.urls import path

from PayRollApp import views

urlpatterns = [
    path("EmployeesList", views.EmployeesList, name="EmployeesList"),
    path("EmployeeDetails/<int:id>", views.EmployeeDetails, name="EmployeeDetails"),
    path("EmployeeDelete/<int:id>/", views.EmployeeDelete, name="EmployeeDelete"),
    path("EmployeeUpdate/<int:id>/", views.EmployeeUpdate, name="EmployeeUpdate"),
    path("EmployeeInsert", views.EmployeeInsert, name="EmployeeInsert"),
    path("BulkEmployeeInsert", views.BulkInsertDemo, name="BID"),
    path("NewBulkInsert", views.NewBulkInsertDemo, name="NewBulkInsert"),
    path("BulkUpdate", views.BulkUpdateDemo, name="BulkUpdate"),
    path("BulkDeleteDemo", views.BulkDeleteDemo, name="BulkDeleteDemo"),
    path("DeleteUsingRadio", views.DeleteUsingRadio, name="DeleteUsingRadio"),
    path("PageWiseEmployees", views.PageWiseEmployeesList, name="PageWiseEmployees"),
    path("cascadingselect/", views.cascadingselect, name="cascadingselect"),
    path("load_states/", views.load_states, name="load_states"),
    path("load_cities/", views.load_cities, name="load_cities"),
    path("TransactionDemo/", views.TransactionDemo, name="TransactionDemo"),
]
