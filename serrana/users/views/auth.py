from django.contrib.auth.views import LoginView, LogoutView

class UserLoginView(LoginView):
    template_name = "auth/login.html"
    redirect_authenticated_user = True
    next_page = "home"
    

class UserLogoutView(LogoutView):
    next_page = "users:login"