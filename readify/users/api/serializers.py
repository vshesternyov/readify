import re

from djoser.conf import settings
from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction

from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, label='Пароль')

    default_error_messages = {
        'cannot_create_user': settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
    }

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'password',)

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get('password')

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {'password': serializer_error['non_field_errors']}
            )

        return attrs

    def validate_phone_number(self, phone_number):
        pattern = re.compile(r'^(0\d{9})$')

        if not pattern.match(phone_number):
            raise serializers.ValidationError(
                'Неправильний номер телефону. Введіть номер у форматі: "0xxxxxxxxx".'
            )

        return phone_number

    def create(self, validated_data):

        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail('cannot_create_user')

        return user

    def perform_create(self, validated_data):

        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=['is_active'])

        return user
