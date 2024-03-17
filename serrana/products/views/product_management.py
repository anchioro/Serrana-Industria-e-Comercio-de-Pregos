from django.db.models import Q
from django.shortcuts import get_object_or_404
from products.models.product import Product
from products.forms.product import ProductForm
from products.models.product import ProductAction, ProductChangeLog
from products.forms.action import ActionForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from re import match


# Create your views here.
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    paginate_by = 25
    template_name = "products/index.html"
    ordering = "-id"
    
class ProductSearchView(LoginRequiredMixin, ListView):
    model = Product
    paginate_by = 25
    template_name = "products/index.html"
    ordering = "-id"
    
    def get_queryset(self):
        search_value = self.request.GET.get("q").strip()
        
        if search_value:
            search_terms = search_value.split()
            
            name_query = Q()
            diameter_query = Q()

            for term in search_terms:
                term = term.lower()
                if match(r"^\d*(x\d*)?\s?(g|kg|unidades|uni)?$", term):
                    diameter_query |= Q(product_diameter__icontains=term) | Q(product_weight__icontains=term)
                else:
                    name_query &= Q(product_name__icontains=term)
               
            combined_query = name_query & diameter_query
            
            results = Product.objects.filter(combined_query).order_by("-id")
            
            if not results:
                return Product.objects.filter(
                    Q(product_name__icontains=search_value) |
                    Q(product_diameter__icontains=search_value) |
                    Q(product_weight__icontains=search_value) |
                    Q(product_quantity__icontains=search_value) | 
                    Q(storage_location__icontains=search_value) |
                    Q(product_status__icontains=search_value)
                ).order_by("-id")
            
            return results
        
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

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/create.html"
    success_url = reverse_lazy("products:index")
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/update.html"
    success_url = reverse_lazy("products:index")
    
    def form_valid(self, form):
        instance = form.instance
        original_instance = form.Meta.model.objects.get(pk=instance.pk)
        with transaction.atomic():
            response = super().form_valid(form)
            
            if form.is_valid():
                form.save()
                
                changed_fields = {}
                for field in form.fields:
                    original_value = getattr(original_instance, field)
                    modified_value = getattr(instance, field)
                    
                    if original_value != modified_value:
                        changed_fields[field] = {
                            "original_value": original_value,
                            "modified_value": modified_value
                        }
                
                if changed_fields:
                    product_action = ProductAction.objects.create(
                    product = form.instance,
                    action = "edit",
                    created_at = timezone.now(),
                    created_by = self.request.user,
                    )
                
                    product_action.save()
                    
                    for field_name, values in changed_fields.items():
                        log_entry = ProductChangeLog.objects.create(
                        product_action=product_action,
                        field_name=field_name,
                        original_value=str(values["original_value"]),
                        modified_value=str(values["modified_value"]),
                        )
                        
                        log_entry.save()
                
            return response

    
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("products:index")
    
class ProductHistoryView(LoginRequiredMixin, ListView):
    model = ProductAction
    paginate_by = 25
    template_name = "products/history.html"

    def get_queryset(self):
        return ProductAction.objects.filter(product__slug=self.kwargs["slug"]).order_by("-created_at")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, slug=self.kwargs["slug"])
        product_actions = self.get_queryset()
        
        product_change_logs = []
        for action in product_actions:
            logs = action.productchangelog_set.all()
            product_change_logs.extend(logs)

        context["product"] = product
        context["change_log"] = product_change_logs
        return context

class ProductActionView(LoginRequiredMixin, CreateView):
    model = ProductAction
    form_class = ActionForm
    template_name = "actions/action.html"
    
    def form_valid(self, form):
        product = get_object_or_404(Product, slug=self.kwargs["slug"])
        
        form.instance.product = product
        form.instance.created_by = self.request.user
        
        return super().form_valid(form)
    
    def get_queryset(self):
        return Product.objects.filter(slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["product"] = product
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        product = get_object_or_404(Product, slug=self.kwargs["slug"])
        kwargs["product"] = product
        return kwargs
    
    def get_success_url(self):
        return reverse_lazy("products:history", kwargs={"slug": self.kwargs["slug"]})
    