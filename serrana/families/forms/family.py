from django import forms
from families.models.family import Family, FamilyContactInformation

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
        
class FamilyContactInformationForm(forms.ModelForm):
    class Meta:
        model = FamilyContactInformation
        
        exclude = [
            "family",
        ]
        
        labels = {
            "person_name": "Nome Proprietário",
            "phone": "Telefone",
            "cpf": "CPF",
            "email": "E-mail",
            "is_valid_phone_for_payment": "Telefone é válido para realização de pagamento.",
            "is_valid_cpf_for_payment": "CPF é válido para realização de pagamento.",
            "is_valid_email_for_payment": "E-mail é válido para realização de pagamento.",
        }
        
    def __init__(self, *args, **kwargs):
        super(FamilyContactInformationForm, self).__init__(*args, **kwargs)
        self.fields["person_name"].widget.attrs["placeholder"] = "Nome do proprietário"
        self.fields["phone"].widget.attrs["placeholder"] = "Número do proprietário"
        self.fields["cpf"].widget.attrs["placeholder"] = "CPF do proprietário"
        self.fields["email"].widget.attrs["placeholder"] = "E-mail do proprietário"
        
    def clean(self):
        phone = self.cleaned_data.get("phone")
        cpf = self.cleaned_data.get("cpf")
        email = self.cleaned_data.get("email")
        
        if not phone and not cpf and not email:
            self.add_error("phone", "Por favor, forneça pelo menos uma forma de contato.")
            self.add_error("cpf", "Por favor, forneça pelo menos uma forma de contato.")
            self.add_error("email", "Por favor, forneça pelo menos uma forma de contato.")
            
        phone_for_payment = self.cleaned_data.get("is_valid_phone_for_payment")
        cpf_for_payment = self.cleaned_data.get("is_valid_cpf_for_payment")
        email_for_payment = self.cleaned_data.get("is_valid_email_for_payment")
        
        if not phone_for_payment and not cpf_for_payment and not email_for_payment:
            self.add_error("is_valid_phone_for_payment", "Por favor, escolha pelo menos uma forma de pagamento.")
            self.add_error("is_valid_cpf_for_payment", "Por favor, escolha pelo menos uma forma de pagamento.")
            self.add_error("is_valid_email_for_payment", "Por favor, escolha pelo menos uma forma de pagamento.")
            
        if phone_for_payment and not phone:
            self.add_error("is_valid_phone_for_payment", "Você selecionou pagamento via telefone, mas o campo de telefone está vazio.")
        
        if cpf_for_payment and not cpf:
            self.add_error("is_valid_cpf_for_payment", "Você selecionou pagamento via CPF, mas o campo de CPF está vazio.")
            
        if email_for_payment and not email:
            self.add_error("is_valid_email_for_payment", "Você selecionou pagamento via e-mail, mas o campo de e-mail está vazio.")
        
        return super().clean()
