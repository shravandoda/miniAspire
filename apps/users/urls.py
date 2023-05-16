# Third Party
from django.urls import path

# App
from apps.users.views import UserCreateView, UserLoginView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="login"),
    path("login/", UserLoginView.as_view(), name="login"),
]
