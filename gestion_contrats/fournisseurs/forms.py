from django import forms
from .models import JuridiqueFournisseur

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = JuridiqueFournisseur
        exclude = [
            'date_exclusion', 'duree_exclusion', 'date_levee_sanction', 
            'structure_ayant_exclu', 'motifs', 'etat', 'type', 'motifs', 'remarques'
        ] 