from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from users.forms.user import UserForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

class UserListView(LoginRequiredMixin, ListView):
    model = User
    paginate_by = 100
    template_name = "users/index.html"
    ordering = "-last_login"
    
class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = "users/create.html"
    success_url = reverse_lazy("users:index")
    
    def form_valid(self, form):
        super().form_valid(form)
        return super().form_valid(form)
        
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users:index")    
    
class UserSearchView(LoginRequiredMixin, ListView):
    model = User
    paginate_by = 100
    template_name = "users/index.html"
    ordering = "-id"
    
    def get_queryset(self):
        search_value = self.request.GET.get("q").strip()
        
        if search_value:
            return User.objects.filter(
                Q(first_name__icontains=search_value) |
                Q(last_name__icontains=search_value) |
                Q(username__icontains=search_value) |
                Q(is_active__icontains=search_value)
                ).order_by("-id")
        else:
            return User.objects.all()
    
class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("users:index")
    