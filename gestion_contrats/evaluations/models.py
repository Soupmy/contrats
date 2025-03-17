from django.db import models

# Create your models here.

from fournisseurs.models import JuridiqueFournisseur
from contracts.models import Contrat
class EvaluationFournisseur(models.Model):
    id = models.AutoField(primary_key=True)
    id_contrat = models.ForeignKey(Contrat, on_delete=models.CASCADE)
    id_fournisseur = models.ForeignKey(JuridiqueFournisseur, on_delete=models.CASCADE)
    contractant = models.CharField(max_length=255) #possibilité de remplissage auto a partir de Fournisseur(nom du contractant) ?
    ecoute_client = models.IntegerField()
    respect_delais_contract = models.IntegerField()
    respect_des_autres_obligations = models.IntegerField()
    taux_conformite = models.IntegerField()
    flexibilite = models.IntegerField()
    total_evaluation = models.IntegerField()
    remarque = models.TextField(blank=True, null=True)

    # Champ pour suivre qui a fait l'évaluation ???
    #evaluateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='evaluations')
    #date_evaluation = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Evaluation {self.id} - {self.contractant}"