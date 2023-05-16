# Third Party
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# App
from apps.users.models import User

admin.site.register(User, UserAdmin)
