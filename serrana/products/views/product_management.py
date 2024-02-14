from django.db.models import Q
from django.contrib import messages
from products.models.product import Product
from products.forms.product import ProductForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction, IntegrityError


# Create your views here.
class ProductListView(ListView):
    model = Product
    paginate_by = 100
    template_name = "products/index.html"
    ordering = "-id"
    
class ProductSearchView(ListView):
    model = Product
    paginate_by = 100
    template_name = "products/index.html"
    ordering = "-id"
    
    def get_queryset(self):
        search_value = self.request.GET.get("q").strip()
        
        if search_value:
            return Product.objects.filter(
                Q(product_name__icontains=search_value) |
                Q(product_status__icontains=search_value)
            ).order_by("-id")
        
        else:
            return Product.objects.all()

class ProductInformationView(ListView):
    model = Product
    template_name = "products/history.html" 
class ProductHistoryView(ListView):
    model = Product
    template_name = "products/history.html"    
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/create.html"
    success_url = reverse_lazy("products:index")
    
    def form_valid(self, form):
        return super().form_valid(form)
    
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/update.html"
    success_url = reverse_lazy("products:index")
    
    def form_valid(self, form):
        with transaction.atomic():
            response = super().form_valid(form)
            
            if form.is_valid():
                form.save()
                messages.success(self.request, "Produto atualizado com sucesso!")
                return response
            else:
                messages.error(self.request, "Falha ao atualizar o produto.")
                return self.form_invalid(form)
    
class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("products:index")