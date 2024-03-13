from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User

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
    created_at = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.searchable_fields
    
    def _set_min_stock_value(self):
        if not self.product_quantity:
            self.min_stock_quantity = 0
            return
        
        self.min_stock_quantity = self.product_quantity // 2
        
    def _set_max_stock_value(self):
        if not self.product_quantity:
            self.max_stock_quantity = 0
            return
        
        self.max_stock_quantity = self.product_quantity * 1.5
    
    def _get_stock_status(self):
        if not self.product_quantity:
            self.product_status = "Estoque zerado"
        elif self.product_quantity < self.min_stock_quantity:
            self.product_status = "Estoque baixo"  
        elif self.product_quantity > self.max_stock_quantity:
            self.product_status = "Estoque alto"
        else:
            self.product_status = "Com estoque"
        
    def save(self, *args, **kwargs):
        slug_text = f"{self.product_name} {self.storage_location}"
        self.slug = slugify(slug_text)
        
        self.created_at = timezone.now()
        if "request" in kwargs:
            self.created_by = kwargs["request"].user
        
        self._set_min_stock_value()
        self._set_max_stock_value()
        
        self._get_stock_status()
        
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
    invoice = models.IntegerField(unique=True)
    unit = models. CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def save(self, *args, **kwargs):
        self.created_at = timezone.now()
        if "request" in kwargs:
            self.created_by = kwargs["request"].user
        
        if self.action == "entry":
            self.product.modify_quantity(self.quantity)
        elif self.action == "exit" and not self.quantity > self.product.product_quantity:
            self.product.modify_quantity(-self.quantity)
        
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Ação produto"
        verbose_name_plural = "Ações produtos"