from django.db import models
from django.utils.translation import gettext_lazy as _


class Department(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Bo'lim Nomi"))
    employee_limit = models.PositiveIntegerField(verbose_name=_("Maksimal Xodimlar Soni"))

    def __str__(self):
        return self.name
    
    def get_count_calc(self):
        """
        Returns the number of employees that can still be added to the department.
        """
        return self.employee_limit - self.employee_set.count()


class Position(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Lavozim Nomi"))

    def __str__(self):
        return self.name


class Employee(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name=_("Bo'lim"))
    position = models.ForeignKey(Position, on_delete=models.PROTECT, verbose_name=_("Lavozim"))
    name = models.CharField(max_length=255, verbose_name=_("Xodim Ismi"))
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Oylik Maosh"))
    employment_type = models.CharField(max_length=50, verbose_name=_("Ish Turi"))  # Now a plain string
    phone_number = models.CharField(max_length=15, verbose_name=_("Telefon Raqami"))

    def __str__(self):
        return self.name


