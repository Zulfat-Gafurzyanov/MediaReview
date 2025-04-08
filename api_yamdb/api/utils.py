from django.conf import settings
from django.core.mail import send_mail


def send_confirmation_code(email, confirmation_code):
    subject = 'Код подтверждения YaMDb'
    message = f'Ваш код подтверждения YaMDb: {confirmation_code}'

    send_mail(subject, message, settings.EMAIL_HOST_USER,
              [email], fail_silently=False)
