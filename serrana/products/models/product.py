from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify

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
        
        self._set_min_stock_value()
        self._set_max_stock_value()
        
        self._get_stock_status()
        
        super(Product, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        super(Product, self).delete(*args, **kwargs)
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
    