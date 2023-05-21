from django.contrib.auth import get_user_model
from oauth2_provider.models import Application
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "miniAspire.settings")
django.setup()

User = get_user_model()

if not User.objects.filter(username=os.getenv("DJANGO_SUPERUSER_USERNAME")).exists():
    User.objects.create_superuser(
        os.getenv("DJANGO_SUPERUSER_USERNAME"),
        "admin@miniAspire.com",
        os.getenv("DJANGO_SUPERUSER_PASSWORD"),
    )
if not Application.objects.filter(name="miniAspire").exists():
    Application.objects.create(
        user=User.objects.get(username=os.getenv("DJANGO_SUPERUSER_USERNAME")),
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        name="miniAspire",
    )
