LIMIT_USERNAME = 150
LIMIT_EMAIL = 254
OUTPUT_LENGTH = 15
NAME_LENGTH = 256

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLE_CHOICES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)

ROLE_MAX_LENGTH = max(len(role) for role, _ in ROLE_CHOICES)

NOT_ALLOWED_USERNAME = ('me',)
