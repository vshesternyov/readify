import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex=r'^(0\d{9})$',
        message='Неправильний номер телефону. Введіть номер у форматі: "0xxxxxxxxx".'
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Адреса електронної пошти'
    )
    phone_number = models.CharField(
        max_length=10,
        unique=True,
        validators=[phone_regex],
        verbose_name='Номер телефону'
    )
    first_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Ім\'я'
    )
    last_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Прізвище'
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Активний'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Статус персоналу'
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name='Статус суперкористувача'
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата приєднання'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = UserManager()

    class Meta:
        verbose_name = 'користувача'
        verbose_name_plural = 'Користувачі'

    def __str__(self):
        return self.email

    @staticmethod
    def has_perm(perm, obj=None):
        return True

    @staticmethod
    def has_module_perms(app_label):
        return True
