from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, UserRoles


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ("username", "role", "is_staff", "is_active",)
    list_filter = ("role", "is_staff", "is_active",)
    
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("role",)}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "email", "password1", "password2", "role", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )

    search_fields = ("username", "email", "role")
    ordering = ("username",)



admin.site.register(CustomUser, CustomUserAdmin)
