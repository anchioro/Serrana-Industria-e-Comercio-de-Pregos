from django.contrib import admin
from .models.product import Product

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.get_fields()]
    
    exclude = [
        "slug"
    ]
    
    list_filter = [
        "product_diameter",
        "product_weight",
        "product_status",
    ]
    
    search_fields = [
        "product_name",
        "product_diameter",
        "product_weight",
        "product_status",
    ]
    
    list_display_links = [
        "product_name"
    ]
    
    ordering = ["id"]
    
    list_per_page = 100
    list_max_show_all = 1000
    