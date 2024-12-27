from django.shortcuts import render, get_object_or_404, redirect
from .models import Department, Position, Employee
from .forms import DepartmentForm, PositionForm, EmployeeForm

# Department Views
def department_list(request):
    departments = Department.objects.all()
    return render(request, "management/department_list.html", {"departments": departments})


def department_create(request):
    form = DepartmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("department_list")
    return render(request, "management/department_form.html", {"form": form})


def department_edit(request, pk):
    department = get_object_or_404(Department, pk=pk)
    form = DepartmentForm(request.POST or None, instance=department)
    if form.is_valid():
        form.save()
        return redirect("department_list")
    return render(request, "management/department_form.html", {"form": form, "department": department})


def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        department.delete()
        return redirect("department_list")
    return render(request, "management/department_confirm_delete.html", {"department": department})

# Position Views
def position_list(request):
    positions = Position.objects.all()
    return render(request, "management/position_list.html", {"positions": positions})


def position_create(request):
    form = PositionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("position_list")
    return render(request, "management/position_form.html", {"form": form})


def position_edit(request, pk):
    position = get_object_or_404(Position, pk=pk)
    form = PositionForm(request.POST or None, instance=position)
    if form.is_valid():
        form.save()
        return redirect("position_list")
    return render(request, "management/position_form.html", {"form": form, "position": position})


def position_delete(request, pk):
    position = get_object_or_404(Position, pk=pk)
    if request.method == "POST":
        position.delete()
        return redirect("position_list")
    return render(request, "management/position_confirm_delete.html", {"position": position})

# Employee Views
def employee_list(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    employees = Employee.objects.filter(department=department)
    return render(request, "management/employee_list.html", {"department": department, "employees": employees})


def employee_create(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    form = EmployeeForm(request.POST or None, initial={"department": department})
    if form.is_valid():
        form.save()
        return redirect("employee_list", department_id=department.id)
    return render(request, "management/employee_form.html", {"form": form, "department": department})


def employee_edit(request, department_id, pk):
    employee = get_object_or_404(Employee, pk=pk, department_id=department_id)
    form = EmployeeForm(request.POST or None, instance=employee)
    if form.is_valid():
        form.save()
        return redirect("employee_list", department_id=department_id)
    return render(request, "management/employee_form.html", {"form": form, "employee": employee})


def employee_delete(request, department_id, pk):
    department = get_object_or_404(Department, pk=department_id)
    employee = get_object_or_404(Employee, pk=pk, department_id=department_id)
    if request.method == "POST":
        employee.delete()
        return redirect("employee_list", department_id=department_id)
    return render(request, "management/employee_confirm_delete.html", {"employee": employee, "department": department})
