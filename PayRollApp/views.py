from django.shortcuts import redirect, render

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
    print(id)
    employee = Employee.objects.get(id=id)
    TemplateFileName = "PayRollApp/EmployeeDelete.html"
    context = {"employee": employee}
    if request.method == "POST":
        employee.delete()
        return redirect("PayRollApp/EmployeesList.html")
    return render(request, TemplateFileName, context)
