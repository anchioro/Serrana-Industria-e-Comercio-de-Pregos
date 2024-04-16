from django import forms
from stock.models.stock import Stock
from django.core.exceptions import ValidationError
import random

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        
        exclude = [
            "slug",
            "created_at",
            "created_by",
        ]
        
        labels = {
            "product_name": "Nome do produto",
            "product_diameter": "Bitola do produto",
            "storage_location": "Localização no estoque",
            "location_description": "Descrição da localização",
            "product_quantity": "Quantidade em estoque",
        }
    
    @staticmethod
    def __random_choice_to_placeholder(choice: str):
        PRODUCT_NAME = [
            "Ardox Polido",
            "Farpado Polido",
            "Ardox Galvanizado",
            "Farpado Galvanizado"
            ]
        PRODUCT_DIAMETER = [
            "18x30",
            "18x36",
            "16x24",
            "17x36"
        ]
        STORAGE_LOCATION = [
            "A1",
            "A2",
            "B1",
            "B2"
        ]
        if choice == "product_name":
            result = random.choice(PRODUCT_NAME)
        elif choice == "product_diameter":
            result = random.choice(PRODUCT_DIAMETER)
        elif choice == "storage_location":
            result = random.choice(STORAGE_LOCATION)
        else:
            result = random.randint(5, 25)
            
        return result
    
    def __init__(self, *args, **kwargs):
        super(StockForm, self).__init__(*args, **kwargs)
        self.fields["product_name"].widget.attrs["placeholder"] = self.__random_choice_to_placeholder("product_name")
        self.fields["product_diameter"].widget.attrs["placeholder"] = self.__random_choice_to_placeholder("product_diameter")
        self.fields["product_quantity"].widget.attrs["placeholder"] = self.__random_choice_to_placeholder("product_quantity")
        self.fields["storage_location"].widget.attrs["placeholder"] = self.__random_choice_to_placeholder("storage_location")
        self.fields["location_description"].widget.attrs["placeholder"] = "Digite uma descrição..."
        
    def clean(self):
        storage_location = self.cleaned_data.get("storage_location")
        
        if Stock.objects.filter(storage_location=storage_location).exists() and self.instance._state.adding:
            self.add_error("storage_location", "Lote já existente neste local.")
        
        return super().clean()