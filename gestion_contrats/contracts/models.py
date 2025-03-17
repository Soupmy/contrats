from django.db import models
from fournisseurs.models import JuridiqueFournisseur

class Contrat(models.Model):
    copie_du_contrat = models.FileField(upload_to='contrats/', blank=True, null=True)
    date_exp_du_contrat = models.DateField()
    lettre_de_prolongation = models.FileField(upload_to='prolongations/', blank=True, null=True)
    recours = models.CharField(max_length=255, blank=True, null=True)
    reference_du_contrat = models.CharField(max_length=100, unique=True)
    la_monnai = models.CharField(max_length=50)
    la_taxe = models.DecimalField(max_digits=10, decimal_places=2)
    montant_contrat_devise = models.DecimalField(max_digits=15, decimal_places=2)
    montant_contrat_da = models.DecimalField(max_digits=15, decimal_places=2)
    type_du_contrat = models.CharField(max_length=100)
    date_saisie_contract = models.DateField()
    filiale = models.CharField(max_length=100)
    duree_attrib_contrat = models.CharField(max_length=50)
    date_install_equip = models.DateField(blank=True, null=True)
    fournisseur = models.ForeignKey(JuridiqueFournisseur, on_delete=models.CASCADE)

    def __str__(self):
        return self.reference_du_contrat
