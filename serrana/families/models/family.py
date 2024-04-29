from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from stock.models.stock import Stock

# Create your models here.
class Family(models.Model):
    family_manager = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    number = models.CharField(max_length=10, blank=True, null=True)
    address_description = models.TextField(blank=True, null=True)
    last_delivery = models.DateTimeField(blank=True, null=True)
    last_payment = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.family_manager}"
    
    def save(self, *args, **kwargs):
        slug_text = f"{self.family_manager}"
        self.slug = slugify(slug_text)
        
        self.family_manager = self.family_manager.title()
        
        if "request" in kwargs:
            self.created_by = kwargs["request"].user
        
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        super(Family, self).delete(*args, **kwargs)
    
    class Meta:
        verbose_name = "Família"
        verbose_name_plural = "Famílias"
      
@staticmethod
def _get_product_choices():
    product_choices = []
    
    for stock in Stock.objects.all():
        product_choices.append((f"{stock.product_name} | {stock.product_diameter}", f"{stock.product_name} | {stock.product_diameter}"))

    return tuple(product_choices)

@staticmethod
def _get_packing_choices():
    packing_choices = []

    for stock in Stock.objects.all():
        packing_option_1kg = f"{stock.product_name} | {stock.product_diameter} | 1 Kg"
        packing_option_500kg = f"{stock.product_name} | {stock.product_diameter} | 500g"
        packing_choices.append((packing_option_1kg, packing_option_1kg))
        packing_choices.append((packing_option_500kg, packing_option_500kg))

    return tuple(packing_choices)
    
class FamilyAction(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    product = models.CharField(max_length=255, choices=_get_product_choices())
    product_packing = models.CharField(max_length=255, choices=_get_packing_choices())
    product_quantity = models.IntegerField(default=0, validators=[MinValueValidator(1)])
    rubber_quantity = models.IntegerField(default=0)
    metal_quantity = models.IntegerField(default=0)
    is_finished = models.BooleanField(default=False)
    status = models.CharField(max_length=255, default="Pendente")
    finished_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if "request" in kwargs:
            self.created_by = kwargs["request"].user
            
        super().save(*args, **kwargs)
        
        self.family.last_delivery = self.created_at
        self.family.save()
        
class FamilyContactInformation(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    cpf = models.CharField(max_length=20, unique=True, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_valid_phone_for_payment = models.BooleanField(default=False)
    is_valid_cpf_for_payment = models.BooleanField(default=False)
    is_valid_email_for_payment = models.BooleanField(default=False)