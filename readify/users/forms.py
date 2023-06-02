from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Ім\'я')
    last_name = forms.CharField(max_length=30, required=True, label='Фамілія')

    class Meta:
        model = User
        fields = ('email',)
