from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User
from .forms import CustomUserCreationForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ('id',)
    list_filter = ('is_active', 'is_staff')
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ('groups', 'user_permissions')
    search_fields = ('email', 'phone_number', 'first_name', 'last_name')
    list_display = ('id', 'email', 'phone_number', 'is_staff', 'is_active')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        # django doesn't translate the last field (dates) correctly, so it was translated manually
        (_('Дати'), {'fields': ('last_login', 'date_joined')}),
    )
    add_form = CustomUserCreationForm
    add_form_template = 'overridden_django_templates/add_form.html'
    delete_confirmation_template = 'overridden_django_templates/delete_confirmation.html'
    delete_selected_confirmation_template = 'overridden_django_templates/delete_selected_confirmation.html'

    # django doesn't translate this message, so it was translated manually also
    def message_user(self, request, message, level='success', extra_tags='', fail_silently=False):
        super().message_user(request, 'Операція завершена успішно', level=level)
