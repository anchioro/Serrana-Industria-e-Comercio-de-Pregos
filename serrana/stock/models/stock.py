from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Stock(models.Model):
    product_name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, blank=True)
    product_diameter = models.CharField(max_length=255)
    storage_location = models.CharField(max_length=255, unique=True)
    location_description = models.TextField(blank=True, null=True)
    product_quantity = models.IntegerField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.product_name}, {self.product_codebar}, {self.product_diameter}, {self.product_weight}, {self.storage_location}"
        
    def save(self, *args, **kwargs):
        slug_text = f"{self.product_name} {self.storage_location}"
        self.slug = slugify(slug_text)
        
        self.product_name = self.product_name.title()
        
        if "request" in kwargs:
            self.created_by = kwargs["request"].user
        
        super().save(*args, **kwargs)
        
    def modify_quantity(self, quantity_change):
        self.product_quantity += quantity_change
        self.save(update_fields=["product_quantity"])
    
    def delete(self, *args, **kwargs):
        super(Stock, self).delete(*args, **kwargs)
        
    class Meta:
        verbose_name = "Estoque"

@receiver(post_save, sender=Stock)
def create_stock_action(sender, instance, created, **kwargs):
    if created:
        user = User.objects.first()

        StockAction.objects.create(
            product=instance,
            action="creation",
            created_at=timezone.now(),
            created_by=user,
        )
class StockAction(models.Model):
    ACTION_CHOICES = (
        ("entry", "Entrada"),
        ("exit", "Saída"),
    )
    
    product = models.ForeignKey(Stock, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(1)])
    family = models.IntegerField(unique=True, null=True)  # Need to be changed to the Foreign Key of the "famílias" when action is "exit"
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if "request" in kwargs:
            self.created_by = kwargs["request"].user
        
        if self.action == "entry":
            self.product.modify_quantity(self.quantity)
        elif self.action == "exit" and not self.quantity > self.product.product_quantity:
            self.product.modify_quantity(-self.quantity)
        
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Ação estoque"
        
class StockChangeLog(models.Model):
    stock_action = models.ForeignKey(StockAction, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=255)
    original_value = models.TextField()
    modified_value = models.TextField()
