from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import ValidationError as DjangoValidationError
from rest_framework import serializers

from api.constants import NOT_ALLOWED_USERNAME


def user_validator(value):
    if value.lower() in NOT_ALLOWED_USERNAME:
        raise ValidationError(f'{value} не может стать именем пользователя.')
    try:
        UnicodeUsernameValidator()(value)
    except DjangoValidationError as e:
        raise serializers.ValidationError(e.message)
