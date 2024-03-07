from django.urls import path
from .views.user_management import UserListView, UserCreateView, UserUpdateView, UserDeleteView, UserSearchView
from .views.auth import UserLoginView, UserLogoutView

app_name = "users"
urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("usuarios/", UserListView.as_view(), name="index"),
    path("usuarios/search/", UserSearchView.as_view(), name="search"),
    path("usuarios/cadastro/", UserCreateView.as_view(), name="create"),
    path("usuarios/<int:pk>/edit/", UserUpdateView.as_view(), name="update"),
    path("usuarios/<int:pk>/delete/", UserDeleteView.as_view(), name="delete"),
]