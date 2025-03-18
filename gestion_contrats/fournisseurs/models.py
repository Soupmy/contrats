from django.db import models

# Create your models here.

class JuridiqueFournisseur(models.Model):

     # Choix pour les champs enum
    ETAT_CHOICES = [
        ('HABILITE', 'Habilité'),
        ('BLACKLISTE', 'Blacklisté'),
    ]

    id = models.AutoField(primary_key=True)
    nom_du_contractant = models.CharField(max_length=255)
    num_fixe = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    nif = models.CharField(max_length=20, blank=True, null=True)
    date_exclusion = models.DateField(blank=True, null=True)
    duree_exclusion = models.CharField(max_length=50, blank=True, null=True)
    date_levee_sanction = models.DateField(blank=True, null=True)
    etat = models.CharField(max_length=50, choices=ETAT_CHOICES, default='HABILITE')  # etat du fournisseur blacklisté ou (par défaut habilité)
    type = models.CharField(max_length=50, blank=True, null=True)
    structure_ayant_exclu = models.CharField(max_length=255, blank=True, null=True)
    motifs = models.TextField(blank=True, null=True)
    remarques = models.TextField(blank=True, null=True)
    activite = models.CharField(max_length=255, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    code_postal = models.CharField(max_length=20, blank=True, null=True)
    wilaya = models.CharField(max_length=100, blank=True, null=True)
    n_identification_fiscale = models.CharField(max_length=50, blank=True, null=True)
    n_identification_statistique = models.CharField(max_length=50, blank=True, null=True)
    n_registre_commerce = models.CharField(max_length=50, blank=True, null=True)
    article_imposition = models.CharField(max_length=50, blank=True, null=True)
    systeme_numerotation_universel = models.CharField(max_length=50, blank=True, null=True)
    carte_artisant = models.CharField(max_length=50, blank=True, null=True)
    num_agrement = models.CharField(max_length=50, blank=True, null=True)
    crit_rech_1 = models.CharField(max_length=255, blank=True, null=True)
    rue = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    telephone_2 = models.CharField(max_length=20, blank=True, null=True)
    forme_jurdique = models.CharField(max_length=100, blank=True, null=True)
    branche = models.CharField(max_length=100, blank=True, null=True)
    type_partenaire = models.CharField(max_length=100, blank=True, null=True)
    cle_pays_banque = models.CharField(max_length=10, blank=True, null=True)
    cle_bancaire = models.CharField(max_length=10, blank=True, null=True)
    compte_bancaire = models.CharField(max_length=20, blank=True, null=True)
    cle_controle_bancaire = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.nom_du_contractant
    
