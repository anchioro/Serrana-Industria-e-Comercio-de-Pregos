from django import forms
from products.models.product import Product
import random

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        
        exclude = [
            "slug"
        ]
        
        labels = {
            "product_name": "Nome do produto",
            "product_codebar": "Código de barras",
            "product_diameter": "Bitola do produto",
            "product_weight": "Peso da embalagem",
            "storage_location": "Localização no estoque",
            "location_description": "Descrição da localização",
            "product_quantity": "Quantidade em estoque",
            "min_stock_quantity": "Estoque mínimo",
            "max_stock_quantity": "Estoque máximo",
            "product_status": "Status"
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
        PRODUCT_WEIGHT = [
            "1 Kg",
            "500 g"
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
        elif choice == "product_weight":
            result = random.choice(PRODUCT_WEIGHT)
        elif choice == "storage_location":
            result = random.choice(STORAGE_LOCATION)
        else:
            result = random.randint(5, 25)
            
        return result
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields["product_name"].widget.attrs["placeholder"] = self.__random_choice_to_placeholder("product_name")
        self.fields["product_diameter"].widget.attrs["placeholder"] = self.__random_choice_to_placeholder("product_diameter")
        self.fields["product_weight"].widget.attrs["placeholder"] = self.__random_choice_to_placeholder("product_weight")
        self.fields["product_quantity"].widget.attrs["placeholder"] = self.__random_choice_to_placeholder("product_quantity")
        self.fields["storage_location"].widget.attrs["placeholder"] = self.__random_choice_to_placeholder("storage_location")
        self.fields["location_description"].widget.attrs["placeholder"] = "Digite uma descrição..."
        
