from django import forms
from stock.models.stock import StockAction
from django.core.exceptions import ValidationError

class StockActionForm(forms.ModelForm):
    class Meta:
        model = StockAction
        
        fields = [
            "action",
            "quantity",
            "family",  # Update the fields as per your requirements
        ]
        
        labels = {
            "action": "Ação",
            "quantity": "Quantidade",
            "family": "Código Família",
        }

    def __init__(self, *args, **kwargs):
        product = kwargs.pop("product", None)
        
        super().__init__(*args, **kwargs)
        
        if product:
            self.product = product
        
        if self.instance:
            if self.instance.action == "exit":
                self.fields["family"].required = True
            else:
                self.fields["family"].required = False
                
    def clean(self):
        action = self.cleaned_data.get("action")
        family = self.cleaned_data.get("family")  # Update to match the field name in the StockAction model
        
        if action == "entry" and family:
            self.add_error("family", ValidationError("Não é possível realizar a entrada de produtos fornecendo um código fiscal."))
        elif action == "exit" and not family:
            self.add_error("family", ValidationError("Não é possível realizar a saída de produtos sem fornecer um código fiscal."))
        else:
            if action == "exit" and StockAction.objects.filter(family=family).exists():
                self.add_error("family", "Código fiscal já utilizado.")
        
        quantity = self.cleaned_data.get("quantity")
        if hasattr(self, "product") and action == "exit" and quantity > self.product.product_quantity:
            self.add_error("quantity", ValidationError(f"O estoque atual do produto é de {self.product.product_quantity}."))
        
        return super().clean()
