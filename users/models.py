from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class UserRoles(models.TextChoices):
    SELLER = "seller", _("Sotuvchi")
    DELIVERY = "delivery", _("Yetkazib beruvchi")


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=UserRoles.choices,
        default=UserRoles.SELLER,
        verbose_name=_("Roli"),
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
