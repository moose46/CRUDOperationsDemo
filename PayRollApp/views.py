from django.shortcuts import redirect, render

from PayRollApp.forms import EmployeeForm
from PayRollApp.models import Employee


# Create your views here.
def EmployeesList(request):
    Employees = Employee.objects.all()
    TemplateFileName = "PayRollApp/EmployeesList.html"
    context = {"Employees": Employees}
    return render(request, TemplateFileName, context)


def EmployeeDetails(request, id):
    employee = Employee.objects.get(id=id)
    TemplateFileName = "PayRollApp/EmployeeDetails.html"
    context = {"employee": employee}
    return render(request, TemplateFileName, context)


def EmployeeDelete(request, id):
    employee = Employee.objects.get(id=id)
    TemplateFileName = "PayRollApp/EmployeeDelete.html"
    context = {"employee": employee}
    if request.method == "POST":
        employee.delete()
        return redirect("EmployeesList")
    return render(request, TemplateFileName, context)


def EmployeeUpdate(request, id):
    TemplateFileName = "PayRollApp/EmployeeUpdate.html"
    employee = Employee.objects.get(id=id)
    form = EmployeeForm(instance=employee)
    context = {"form": form}
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        print(f"the form is valid {form.is_valid()}")
        if form.is_valid():
            form.save()
        return redirect("EmployeesList")
    return render(request, TemplateFileName, context)
