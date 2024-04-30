from django.conf import settings
from django.core.paginator import PageNotAnInteger, Paginator
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render

from PayRollApp.forms import (
    EmployeeForm,
    OnSiteEmployeesForm,
    PartTimeEmployeeForm,
    PartTimeEmployeeFormSet,
)
from PayRollApp.models import City, Employee, PartTimeEmployee, State


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


def PageWiseEmployeesList(request):
    page_size = int(request.GET.get("page_size", getattr(settings, "PAGE_SIZE", 5)))
    page = request.GET.get("page", 1)

    search_query = request.GET.get("search", "")

    sort_by = request.GET.get("sort_by", "id")
    sort_order = request.GET.get("sort_order", "asc")

    valid_sort_fields = ["id", "FirstName", "LastName", "TitleName"]
    if sort_by not in valid_sort_fields:
        sort_by = "id"

    employees = PartTimeEmployee.objects.filter(
        Q(id__icontains=search_query)
        | Q(FirstName__icontains=search_query)
        | Q(LastName__icontains=search_query)
        | Q(TitleName__icontains=search_query)
    )
    # apply sorting
    if sort_order == "desc":
        employees.order_by(f"-{sort_by}")
    else:
        employees.order_by(f"{sort_by}")
    # employees = PartTimeEmployee.objects.all()
    pageinator = Paginator(employees, page_size)
    try:
        employees_page = pageinator.page(page)
    except PageNotAnInteger:
        employees_page = pageinator.page(1)
    return render(
        request,
        "PayRollApp/PageWiseEmployees.html",
        context={
            "employees_page": employees_page,
            "page_size": page_size,
            "search_query": search_query,
            "sort_by": sort_by,
            "sort_order": sort_order,
        },
    )


def cascadingselect(request):
    employee_form = OnSiteEmployeesForm()

    if request.method == "POST":
        employee_form = OnSiteEmployeesForm(request.POST)
        if employee_form.is_valid():
            employee_form.save()
            return JsonResponse({"success": True})
    return render(
        request, "PayRollAPp/CascadingDemo.html", {"employee_form": employee_form}
    )


def load_states(request):
    country_id = request.GET.get("country_id")
    states = State.objects.filter(country_id=country_id).values("id", "name")
    return JsonResponse(list(states), safe=False)


def load_cities(request):
    state_id = request.GET.get("state_id")
    cities = City.objects.filter(state_id=state_id).values("id", "name")
    return JsonResponse(list(cities), safe=False)


def TransactionDemo(request):
    try:
        with transaction.atomic():
            employee = PartTimeEmployee.objects.create(
                FirstName="Bob", LastName="Culbertson", TitleName="Friend"
            )
            employee = PartTimeEmployee.objects.create(
                FirstName="Shane", LastName="McQuire", TitleName="Friend"
            )
            employee = PartTimeEmployee.objects.create(
                FirstName="Bill", LastName="Verhoff", TitleName="Friend"
            )
            employee = PartTimeEmployee.objects.create(
                FirstName="Robin", LastName="Leonard", TitleName="Boxer"
            )
            employee = PartTimeEmployee.objects.create(
                FirstName="Bill", Lastame="Sweeney", TitleName="Salesman"
            )
    except Exception as e:
        return render(request, "PayRollApp/TransactionDemo.html", {"Message": str(e)})
    return render(request, "PayRollApp/TransactionDemo.html", {"Message": "Success!!!"})
