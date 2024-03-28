from django.db import models
from django.db.models import Sum, Avg
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from datetime import timedelta
from statistics import stdev

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_codebar = models.CharField(max_length=13, unique=True)
    slug = models.CharField(max_length=255, blank=True)
    product_diameter = models.CharField(max_length=255)
    product_weight = models.CharField(max_length=255)
    storage_location = models.CharField(max_length=255, unique=True)
    location_description = models.TextField(blank=True, null=True)
    product_quantity = models.IntegerField(validators=[MinValueValidator(0)])
    min_stock_quantity = models.IntegerField(blank=True, null=True)
    max_stock_quantity = models.IntegerField(blank=True, null=True)
    product_status = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.product_name}, {self.product_codebar}, {self.product_diameter}, {self.product_weight}, {self.storage_location}"
        
    def save(self, *args, **kwargs):
        slug_text = f"{self.product_name} {self.storage_location}"
        self.slug = slugify(slug_text)
        
        if "request" in kwargs:
            self.created_by = kwargs["request"].user
        
        super().save(*args, **kwargs)
    
    def modify_quantity(self, quantity_change):
        self.product_quantity += quantity_change
        self.save(update_fields=["product_quantity"])
    
    def delete(self, *args, **kwargs):
        super(Product, self).delete(*args, **kwargs)
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
    
class ProductAction(models.Model):
    ACTION_CHOICES = (
        ("entry", "Entrada"),
        ("exit", "Saída"),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(1)])
    invoice = models.IntegerField(unique=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
        
    def _set_min_stock_value(self):
        MONTH = 30
        Z = 1.65
        
        start_date = timezone.now() - timedelta(days=MONTH)
        end_date = timezone.now()

        total_demand_quantity = ProductAction.objects.filter(
            product=self.product,
            action="exit",
            created_at__range=(start_date, end_date)
        ).aggregate(Sum("quantity"))["quantity__sum"]
        
        if total_demand_quantity is None:
            total_demand_quantity = 0
            
        average_daily_demand = total_demand_quantity / MONTH
        
        daily_demand = [action.quantity for action in ProductAction.objects.filter(
            product=self.product,
            action="exit",
            created_at__range=(timezone.now() - timedelta(days=1), end_date)
        )]
        
        if len(daily_demand) > 1:
            demand_stdev = stdev(daily_demand)
        else:
            demand_stdev = 0
        
        security_stock = Z * demand_stdev
        
        min_stock = average_daily_demand + security_stock
        
        if min_stock:
            self.product.min_stock_quantity = min_stock
        else:
            self.product.min_stock_quantity = 0
        
        self.product.save()
        
    def _set_max_stock_value(self):
        min_stock = self.product.min_stock_quantity
        
        self.product.max_stock_quantity = min_stock + min_stock * .5
        
        self.product.save()
    
    def _get_stock_status(self):
        min_stock = self.product.min_stock_quantity
        max_stock = self.product.max_stock_quantity
        current_stock = self.product.product_quantity
        
        if not min_stock:
            self.product.product_status = "Sem estoque mínimo definido."
        elif not max_stock:
            self.product.product_status = "Sem estoque máximo definido."
        else:
            if current_stock <= min_stock:
                self.product.product_status = "Abaixo do estoque mínimo."
            elif current_stock >= max_stock:
                self.product.product_status = "Excedeu o estoque máximo."
            else:
                self.product.product_status = "Com estoque suficiente."
            
        self.product.save()
    
    def save(self, *args, **kwargs):
        if "request" in kwargs:
            self.created_by = kwargs["request"].user
        
        if self.action == "entry":
            self.product.modify_quantity(self.quantity)
        elif self.action == "exit" and not self.quantity > self.product.product_quantity:
            self.product.modify_quantity(-self.quantity)
            
        super().save(*args, **kwargs)
        
        self._set_min_stock_value()
        self._set_max_stock_value()
        
        self._get_stock_status()
        
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Ação produto"
        verbose_name_plural = "Ações produtos"
        
class ProductChangeLog(models.Model):
    product_action = models.ForeignKey(ProductAction, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=255)
    original_value = models.TextField()
    modified_value = models.TextField()
