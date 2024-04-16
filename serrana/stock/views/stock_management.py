from django.db.models import Q, Max, OuterRef
from django.shortcuts import get_object_or_404
from stock.models.stock import Stock, StockAction, StockChangeLog
from stock.forms.stock import StockForm
from stock.forms.action import StockActionForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from re import match

# Create your views here.
class StockListView(LoginRequiredMixin, ListView):
    model = Stock
    paginate_by = 25
    template_name = "stock/index.html"

    def get_queryset(self):
        latest_actions_subquery = StockAction.objects.filter(
            product_id=OuterRef("id")
        ).values("product_id").annotate(
            latest_action=Max("created_at")
        ).values("latest_action")
        
        queryset = Stock.objects.annotate(
            latest_action=latest_actions_subquery
        ).order_by("-latest_action").distinct()
        
        return queryset
    
class StockSearchView(LoginRequiredMixin, ListView):
    model = Stock
    paginate_by = 25
    template_name = "stock/index.html"
    ordering = "-id"
    
    def get_queryset(self):
        search_value = self.request.GET.get("q").strip()
        
        if search_value:
            search_terms = search_value.split()
            
            name_query = Q()
            diameter_query = Q()

            for term in search_terms:
                term = term.lower()
                if match(r"^\d*(x\d*)?\s?(g|kg|unidades|uni)?$", term):  # Need to be changed to a regex that matches the stock information
                    diameter_query = Q(product_diameter__icontains=term)
                else:
                    name_query &= Q(product_name__icontains=term)
               
            combined_query = name_query & diameter_query
            
            results = Stock.objects.filter(combined_query).order_by("-id")
            
            if not results:
                return Stock.objects.filter(
                    Q(product_name__icontains=search_value) |
                    Q(product_diameter__icontains=search_value) |
                    Q(product_quantity__icontains=search_value) | 
                    Q(storage_location__icontains=search_value)
                ).order_by("-id")
            
            return results
        
        else:
            latest_actions_subquery = StockAction.objects.filter(
                product_id=OuterRef("id")
            ).values("product_id").annotate(
                latest_action=Max("created_at")
            ).values("latest_action")
            
            queryset = Stock.objects.annotate(
                latest_action=latest_actions_subquery
            ).order_by("-latest_action").distinct()
            
            return queryset

class StockCreateView(LoginRequiredMixin, CreateView):
    model = Stock
    form_class = StockForm
    template_name = "stock/create.html"
    success_url = reverse_lazy("stock:index")
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class StockUpdateView(LoginRequiredMixin, UpdateView):
    model = Stock
    form_class = StockForm
    template_name = "stock/update.html"
    success_url = reverse_lazy("stock:index")
    
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
                    stock_action = StockAction.objects.create(
                    product = instance,
                    action = "edit",
                    created_at = timezone.now(),
                    created_by = self.request.user,
                    )
                
                    stock_action.save()
                    
                    for field_name, values in changed_fields.items():
                        log_entry = StockChangeLog.objects.create(
                        stock_action=stock_action,
                        field_name=field_name,
                        original_value=str(values["original_value"]),
                        modified_value=str(values["modified_value"]),
                        )
                        
                        log_entry.save()
                
            return response
    
class StockDeleteView(LoginRequiredMixin, DeleteView):
    model = Stock
    success_url = reverse_lazy("stock:index")

class StockHistoryView(LoginRequiredMixin, ListView):
    model = StockAction
    paginate_by = 25
    template_name = "stock/history.html"

    log_field_display_names = {
        "product_name": "Nome do produto",
        "product_diameter": "Bitola do produto",
        "product_quantity": "Quantidade do produto",
        "storage_location": "Estoque físico",
    }

    def get_queryset(self):
        return StockAction.objects.filter(product__slug=self.kwargs["slug"]).order_by("-created_at")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock = get_object_or_404(Stock, slug=self.kwargs["slug"])
        stock_actions = self.get_queryset()
        
        stock_change_logs = []
        for action in stock_actions:
            logs = action.stockchangelog_set.all()
            stock_change_logs.extend(logs)

        context["product"] = stock
        context["change_log"] = stock_change_logs
        context["log_field_display_names"] = self.log_field_display_names
        return context
    
class StockInformationView(LoginRequiredMixin, DetailView):
    model = Stock
    template_name = "stock/information.html"
    context_object_name = "stock"
    slug_field = "slug"

    def get_queryset(self):
        return Stock.objects.filter(slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["product"] = product
        return context
    
class StockActionView(LoginRequiredMixin, CreateView):
    model = StockAction
    form_class = StockActionForm
    template_name = "stock/action.html"
    
    def form_valid(self, form):
        product = get_object_or_404(Stock, slug=self.kwargs["slug"])
        form.instance.product = product
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    
    def get_queryset(self):
        return Stock.objects.filter(slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["product"] = product
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        product = get_object_or_404(Stock, slug=self.kwargs["slug"])
        kwargs["product"] = product
        return kwargs
    
    def get_success_url(self):
        return reverse_lazy("stock:history", kwargs={"slug": self.kwargs["slug"]})