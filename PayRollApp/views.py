from django.shortcuts import redirect, render

from PayRollApp.forms import EmployeeForm
from PayRollApp.models import Employee


# Create your views here.
def EmployeesList(request):
    # Employees = Employee.objects.all()
    Employees = Employee.objects.select_related("EmpDepartment", "EmpCountry").all()
    # print(Employees.query)
    TemplateFileName = "PayRollApp/EmployeesList.html"
    context = {"Employees": Employees}
    return render(request, TemplateFileName, context)


def EmployeeDetails(request, id):
    # employee = Employee.objects.get(id=id)
    employee = (
        Employee.objects.select_related("EmpDepartment", "EmpCountry")
        .all()
        .filter(id=id)
    )
    TemplateFileName = "PayRollApp/EmployeeDetails.html"
    context = {"employee": employee[0]}
    return render(request, TemplateFileName, context)


def EmployeeDelete(request, id):
    # employee = Employee.objects.get(id=id)
    employee = (
        Employee.objects.select_related("EmpDepartment", "EmpCountry")
        .all()
        .filter(id=id)
    )
    TemplateFileName = "PayRollApp/EmployeeDelete.html"
    context = {"employee": employee[0]}
    if request.method == "POST":
        employee.delete()
        return redirect("EmployeesList")
    return render(request, TemplateFileName, context)


def EmployeeUpdate(request, id):
    TemplateFileName = "PayRollApp/EmployeeUpdate.html"
    # employee = Employee.objects.get(id=id)
    employee = (
        Employee.objects.select_related("EmpDepartment", "EmpCountry")
        .all()
        .filter(id=id)
    )
    form = EmployeeForm(instance=employee[0])
    context = {"form": form}
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee[0])
        print(f"the form is valid {form.is_valid()}")
        if form.is_valid():
            form.save()
        return redirect("EmployeesList")
    return render(request, TemplateFileName, context)


# Function based view
def EmployeeInsert(request):
    TemplateFile = "PayRollApp/EmployeeInsert.html"
    form = EmployeeForm()

    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("EmployeesList")

    return render(request, TemplateFile, {"form": form})
