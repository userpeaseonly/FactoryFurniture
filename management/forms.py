from django import forms
from .models import Department, Position, Employee


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "employee_limit"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "block w-full px-4 py-2 border border-gray-300 rounded-lg",
                "placeholder": "Bo'lim Nomi"
            }),
            "employee_limit": forms.NumberInput(attrs={
                "class": "block w-full px-4 py-2 border border-gray-300 rounded-lg",
                "placeholder": "Maksimal Xodimlar Soni"
            }),
        }


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "block w-full px-4 py-2 border border-gray-300 rounded-lg",
                "placeholder": "Lavozim Nomi"
            }),
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["department", "position", "name", "salary", "employment_type", "phone_number"]
        widgets = {
            "department": forms.Select(attrs={
                "class": "block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500"
            }),
            "position": forms.Select(attrs={
                "class": "block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500"
            }),
            "name": forms.TextInput(attrs={
                "class": "block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500",
                "placeholder": "Xodim Ismi"
            }),
            "salary": forms.NumberInput(attrs={
                "class": "block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500",
                "placeholder": "Oylik Maosh"
            }),
            "employment_type": forms.TextInput(attrs={  # Free text input for employment type
                "class": "block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500",
                "placeholder": "Stavka"
            }),
            "phone_number": forms.TextInput(attrs={
                "class": "block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500",
                "placeholder": "Telefon Raqami"
            }),
        }


class PositionReassignForm(forms.Form):
    new_position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        label="Yangi Lavozim",
        widget=forms.Select(attrs={
            "class": "block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500",
        }),
    )
