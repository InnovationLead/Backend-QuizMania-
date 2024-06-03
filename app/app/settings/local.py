""" Local development Settings """
from .base import *

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
# EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST=os.environ.get('EMAIL_HOST')
EMAIL_USE_TLS=False
EMAIL_PORT=587
EMAIL_HOST_USER=os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL=os.environ.get('DEFAULT_FROM_EMAIL')

# <EMAIL_CONFIRM_REDIRECT_BASE_URL>/<key>
EMAIL_CONFIRM_REDIRECT_BASE_URL=\
    "http://localhost:3000/email/confirm/"

# <PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL>/<uid64>/<token>/
PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL=\
    "http://localhost:3000/password-reset/confirm/"