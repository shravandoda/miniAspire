# Third Party
from django.contrib.auth.models import AbstractUser

# App
from miniAspire.models import BaseModel


class User(AbstractUser, BaseModel):
    pass
