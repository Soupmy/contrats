from django import forms
from .models import Contrat

class ContratForm(forms.ModelForm):
    class Meta:
        model = Contrat
        fields = '__all__'
        widgets = {
            # Widgets pour les champs Date
            'date_prev_attrib_contrat': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_prev_signat_contrat_bon': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_reel_signat_contr_bon': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_prev_notif_attribu': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_reel_notif_attrib': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_prev_signature_contrat': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_reel_sign_cont': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_exp_du_contrat': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_saisie_contract': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'disabled': True}),
            'date_install_equip': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            
            # Widgets pour les champs texte utilisés comme numériques
            'delais_estimatif_execut_livrai': forms.TextInput(attrs={'class': 'form-control'}),
            'delais_execution_livraison': forms.TextInput(attrs={'class': 'form-control'}),
            'duree_contrat': forms.TextInput(attrs={'class': 'form-control'}),
            'duree_attrib_contrat': forms.TextInput(attrs={'class': 'form-control'}),
            
            # Widgets pour les champs Numériques
            'la_taxe': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': False}),
            'montant_contrat_devise': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': False}),
            'montant_contrat_da': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': False}),
            
            # Widgets pour les fichiers
            'dossier_consultation': forms.FileInput(attrs={'class': 'form-control', 'required': False}),
            'pv_ouverture': forms.FileInput(attrs={'class': 'form-control', 'required': False}),
            'pv_attribution_prov_marche': forms.FileInput(attrs={'class': 'form-control', 'required': False}),
            'copie_du_contrat': forms.FileInput(attrs={'class': 'form-control', 'required': False}),
            'lettre_de_prolongation': forms.FileInput(attrs={'class': 'form-control', 'required': False}),
            'lettre_invitation': forms.FileInput(attrs={'class': 'form-control', 'required': False}),
            
            # Widgets pour les champs texte
            'intitul': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'nationalite': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'recours': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'la_monnai': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            
            # Widgets pour les sélecteurs
            'nature': forms.Select(attrs={'class': 'form-control', 'required': False}),
            'type_du_contrat': forms.Select(attrs={'class': 'form-control', 'required': False}),
            'reference_du_contrat': forms.Select(attrs={'class': 'form-control', 'required': False}),
            
            # Widgets pour les clés étrangères
            'id_contractant': forms.Select(attrs={'class': 'form-control', 'required': False}),
            'unite': forms.Select(attrs={'class': 'form-control', 'required': False}),
            'filiale': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre tous les champs optionnels au niveau du formulaire
        for field_name in self.fields:
            self.fields[field_name].required = False
            
        # Organisation des champs par paires thématiques
        self.field_order = [
            # Paire 1 : Identification
            'intitul', 'reference_du_contrat',
            # Paire 2 : Typologie
            'type_du_contrat', 'nature',
            # Paire 3 : Localisation
            'nationalite', 'unite',
            # Paire 4 : Fournisseur
            'id_contractant', 'filiale',
            # Paire 5 : Dates importantes 1
            'date_prev_attrib_contrat', 'date_reel_notif_attrib',
            # Paire 6 : Dates importantes 2
            'date_prev_signature_contrat', 'date_reel_sign_cont',
            # Paire 7 : Durées
            'duree_contrat', 'duree_attrib_contrat',
            # Paire 8 : Financier 1
            'montant_contrat_da', 'montant_contrat_devise',
            # Paire 9 : Financier 2
            'la_taxe', 'la_monnai',
            # Paire 10 : Délais
            'delais_estimatif_execut_livrai', 'delais_execution_livraison',
            # Paire 11 : Documents 1
            'dossier_consultation', 'pv_ouverture',
            # Paire 12 : Documents 2
            'pv_attribution_prov_marche', 'copie_du_contrat',
            # Paire 13 : Documents 3
            'lettre_invitation', 'lettre_de_prolongation',
            # Paire 14 : Divers 
            'recours', 'date_install_equip',
            # Autres champs nécessaires mais moins visibles
            'date_prev_signat_contrat_bon', 'date_reel_signat_contr_bon',
            'date_prev_notif_attribu', 'date_exp_du_contrat', 'date_saisie_contract'
        ]