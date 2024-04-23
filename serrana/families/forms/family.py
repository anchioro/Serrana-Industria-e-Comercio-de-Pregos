from django import forms
from families.models.family import Family

class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        
        exclude = [
            "slug",
            "created_at",
            "created_by",
        ]
        
        labels = {
            "family_manager": "Responsável da Família",
            "zip_code": "CEP",
            "state": "Estado",
            "city": "Cidade",
            "address": "Endereço",
            "number": "Número",
            "address_description": "Informações adicionais",
            "is_active": "Ativo"
        }
    
    def __init__(self, *args, **kwargs):
        super(FamilyForm, self).__init__(*args, **kwargs)
        self.fields["family_manager"].widget.attrs["placeholder"] = "Nome do responsável"
        self.fields["zip_code"].widget.attrs["placeholder"] = "Código postal"
        self.fields["state"].widget.attrs["placeholder"] = "Estado"
        self.fields["city"].widget.attrs["placeholder"] = "Cidade"
        self.fields["address"].widget.attrs["placeholder"] = "Endereço da casa"
        self.fields["number"].widget.attrs["placeholder"] = "Número da casa"
        self.fields["address_description"].widget.attrs["placeholder"] = "Digite informações adicionais do endereço..."
        self.fields["is_active"].widget.attrs["placeholder"] = "Indica que o usuário será tratado como ativo. Ao invés de excluir contas de usuário, desmarque isso."
        