from datetime import datetime

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError

from api.constants import NOT_ALLOWED_USERNAME


def user_validator(value):
    """Валидатор для проверки имени пользователя."""
    if value in NOT_ALLOWED_USERNAME:
        raise ValidationError(f'{value} не может стать именем пользователя.')
    UnicodeUsernameValidator()(value)


def title_year_validator(value):
    """Валидатор для проверки года выпуска произведения."""
    now = datetime.now().year
    if value > now:
        raise ValidationError(
            f'Год выпуска произведения не может быть больше {now} года')
