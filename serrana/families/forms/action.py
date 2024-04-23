from django import forms
from families.models.family import FamilyAction

class FamilyActionForm(forms.ModelForm):
    class Meta:
        model = FamilyAction
        
        fields = [
            "product",
            "product_packing",
            "product_quantity",
            "rubber_quantity",
            "metal_quantity",
            ]
        
        labels = {
            "product": "Produto",
            "product_packing": "Embalagem",
            "product_quantity": "Quantidade Prego",
            "rubber_quantity": "Quantidade Borracha",
            "metal_quantity": "Quantidade Metal", 
        }

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        product_packing = cleaned_data.get("product_packing")
        
        if not product_packing and product:
            self.add_error('product', ('Por favor, selecione um produto.'))

        return cleaned_data

