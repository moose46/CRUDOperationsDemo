from django.shortcuts import redirect, render

from PayRollApp.forms import EmployeeForm, PartTimeEmployeeForm, PartTimeEmployeeFormSet
from PayRollApp.models import Employee, PartTimeEmployee


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


def BulkInsertDemo(request):
    extra_forms = 10
    forms = [
        PartTimeEmployeeForm(request.POST or None, prefix=f"employee-{i}")
        for i in range(extra_forms)
    ]
    Status = ""
    if request.method == "POST":
        for form in forms:
            if form.is_valid() and form.cleaned_data.get("FirstName", ""):
                form.save()
                Status = "Records were inserted successfully..."

    return render(
        request,
        "PayRollApp/parttimeemployee_list.html",
        {"forms": forms, "extra_forms": range(extra_forms), "Status": Status},
    )


def NewBulkInsertDemo(request):

    if request.method == "POST":
        formset = PartTimeEmployeeFormSet(request.POST, prefix="employee")
        if formset.is_valid():
            employees = formset.save(commit=False)
            PartTimeEmployee.objects.bulk_create(employees)
            return redirect("NewBulkInsert")
    else:
        formset = PartTimeEmployeeFormSet(
            queryset=PartTimeEmployee.objects.none(), prefix="employee"
        )
    return render(
        request,
        "PayRollApp/NewBulkInsert.html",
        {"formset": formset},
    )


def BulkUpdateDemo(request):
    employees = PartTimeEmployee.objects.all()
    forms = [
        PartTimeEmployeeForm(
            request.POST or None, instance=employee, prefix=f"employee-{employee.id}"
        )
        for employee in employees
    ]
    if request.method == "POST":
        updated_data = []
        for form in forms:
            if form.is_valid():
                employee = form.instance
                employee.FirstName = form.cleaned_data["FirstName"]
                employee.LastName = form.cleaned_data["LastName"]
                employee.TitleName = form.cleaned_data["TitleName"]
                updated_data.append(employee)
        PartTimeEmployee.objects.bulk_update(
            updated_data, ["FirstName", "LastName", "TitleName"]
        )

    return render(
        request,
        "PayRollApp/BulkUpdateDemo.html",
        {"forms": forms, "employees": employees},
    )


def BulkDeleteDemo(request):
    employees = PartTimeEmployee.objects.all()
    if request.method == "POST":
        if selected_ids := request.POST.getlist("selected_ids"):
            PartTimeEmployee.objects.filter(pk__in=selected_ids).delete()
            return redirect("BulkDeleteDemo")
    return render(
        request,
        "PayRollApp/BulkDelete.html",
        {"employees": employees},
    )


def DeleteUsingRadio(request):
    employees = PartTimeEmployee.objects.all()

    if request.method == "POST":
        if selected_id := request.POST.get("selected_id"):
            PartTimeEmployee.objects.filter(pk=selected_id).delete()
            return redirect("DeleteUsingRadio")

    return render(
        request,
        "PayRollApp/DeleteUsingRadio.html",
        {"employees": employees},
    )
