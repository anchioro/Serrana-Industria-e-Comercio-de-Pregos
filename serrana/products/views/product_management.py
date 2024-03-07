from django.db.models import Q
from products.models.product import Product
from products.forms.product import ProductForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    paginate_by = 100
    template_name = "products/index.html"
    ordering = "-id"
    
class ProductSearchView(LoginRequiredMixin, ListView):
    model = Product
    paginate_by = 100
    template_name = "products/index.html"
    ordering = "-id"
    
    def get_queryset(self):
        search_value = self.request.GET.get("q").strip()
        
        if search_value:
            return Product.objects.filter(
                Q(product_name__icontains=search_value) |
                Q(product_diameter__icontains=search_value) |
                Q(product_weight__icontains=search_value) |
                Q(product_quantity__icontains=search_value) | 
                Q(product_status__icontains=search_value)
            ).order_by("-id")
        
        else:
            return Product.objects.all()

class ProductInformationView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "products/information.html"
    context_object_name = "product"
    slug_field = "slug"

    def get_queryset(self):
        return Product.objects.filter(slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["product"] = product
        return context
    
class ProductHistoryView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "products/history.html"   
    context_object_name = "product"
    slug_field = "slug"
    
    def get_queryset(self):
        return Product.objects.filter(slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["product"] = product
        return context
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/create.html"
    success_url = reverse_lazy("products:index")
    
    def form_valid(self, form):
        return super().form_valid(form)
    
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/update.html"
    success_url = reverse_lazy("products:index")
    
    def form_valid(self, form):
        with transaction.atomic():
            response = super().form_valid(form)
            
            if form.is_valid():
                form.save()
                return response
            else:
                return self.form_invalid(form)
    
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("products:index")