from django.contrib import admin
from .models import Department, Position, Employee


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "employee_limit")
    search_fields = ("name",)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "position", "salary", "employment_type", "phone_number")
    list_filter = ("department", "position", "employment_type")
    search_fields = ("name", "phone_number")
