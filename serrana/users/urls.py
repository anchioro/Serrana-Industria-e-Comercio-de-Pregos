from django.urls import path
from .views.user_management import views

app_name = "users"
urlspatterns = [
    path("", views.index, name="index"),
    path("cadastro/", views.create, name="create"),
    path("login/", views.login, name="login"),
]