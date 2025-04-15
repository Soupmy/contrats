from django import forms
from .models import JuridiqueFournisseur

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = JuridiqueFournisseur
        exclude = [
            'date_exclusion', 'duree_exclusion', 'date_levee_sanction',
            'structure_ayant_exclu', 'motifs', 'etat', 'type', 'remarques'
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'ex: nom@exemple.com', 'required': 'required'}),
            'telephone': forms.TextInput(attrs={'type': 'tel', 'placeholder': 'Ex: 0555 55 55 55', 'required': 'required'}),
            'nif': forms.TextInput(attrs={'pattern': '[0-9]{15}', 'placeholder': 'Numéro NIF à 15 chiffres'}),
            'date_exclusion': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = ['nom_du_contractant', 'num_fixe' , 'email', 'nif', 'activite', 'adresse', 'wilaya', 'ville', 'forme_jurdique', ]
        for name, field in self.fields.items():
            if name in required_fields:
                field.required = True
                field.widget.attrs['required'] = 'required'



class BlacklistFournisseurForm(forms.Form):
    fournisseur = forms.ModelChoiceField(
        queryset=JuridiqueFournisseur.objects.exclude(etat='BLACKLISTE'),
        empty_label="Aucun fournisseur disponible",
        label="Fournisseur à blacklister",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_exclusion = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date d'exclusion"
    )
    duree_exclusion = forms.CharField(
        max_length=100,
        required=False,
        label="Durée d'exclusion"
    )
    motifs = forms.CharField(
        widget=forms.Textarea,
        label="Motifs"
    )

    def clean(self):
        cleaned_data = super().clean()
        blacklist_type = self.data.get('blacklist_type')
        
        if blacklist_type == 'temporaire':
            if not cleaned_data.get('date_exclusion'):
                raise forms.ValidationError("La date d'exclusion est requise pour un blacklistage temporaire")
            if not cleaned_data.get('duree_exclusion'):
                raise forms.ValidationError("La durée d'exclusion est requise pour un blacklistage temporaire")
        
        return cleaned_data