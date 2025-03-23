from django import forms
from .models import JuridiqueFournisseur

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = JuridiqueFournisseur
        fields = '__all__'  # inclure tout les champs dans le form