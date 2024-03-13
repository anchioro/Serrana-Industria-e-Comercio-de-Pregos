from django import forms
from products.models.product import ProductAction
from django.core.exceptions import ValidationError

class ActionForm(forms.ModelForm):
    class Meta:
        model = ProductAction
        
        fields = [
        "action",
        "quantity",
        "invoice",
        "unit",
        ]
        
        labels = {
            "action": "Ação",
            "quantity": "Quantidade",
            "invoice": "Código Nota Fiscal",
            "unit": "Unidade de Medida",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance:
            if self.instance.action == "exit":
                self.fields["invoice"].required = True
            else:
                self.fields["invoice"].required = False
                
    def clean(self):
        action = self.cleaned_data.get("action")
        invoice = self.cleaned_data.get("invoice")
        
        if action == "entry" and invoice:
            self.add_error("invoice", ValidationError("Não é possível realizar a entrada de produtos fornecendo um código fiscal."))
        elif action == "exit" and not invoice:
            self.add_error("invoice", ValidationError("Não é possível realizar a saída de produtos sem fornecer um código fiscal."))
        
        return super().clean()
    