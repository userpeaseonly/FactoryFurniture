from django.urls import path
from . import views


urlpatterns = [
    # Department URLs
    path("departments/", views.department_list, name="department_list"),
    path("departments/create/", views.department_create, name="department_create"),
    path("departments/edit/<int:pk>/", views.department_edit, name="department_edit"),
    path("departments/delete/<int:pk>/", views.department_delete, name="department_delete"),

    # Position URLs
    path("positions/", views.position_list, name="position_list"),
    path("positions/create/", views.position_create, name="position_create"),
    path("positions/edit/<int:pk>/", views.position_edit, name="position_edit"),
    path("positions/delete/<int:pk>/", views.position_delete, name="position_delete"),
    path("positions/reassign/<int:pk>/", views.position_reassign, name="position_reassign"),

    # Employee URLs
    path("departments/<int:department_id>/employees/", views.employee_list, name="employee_list"),
    path("departments/<int:department_id>/employees/create/", views.employee_create, name="employee_create"),
    path("departments/<int:department_id>/employees/edit/<int:pk>/", views.employee_edit, name="employee_edit"),
    path("departments/<int:department_id>/employees/delete/<int:pk>/", views.employee_delete, name="employee_delete"),
]
