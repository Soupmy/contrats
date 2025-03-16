from django.db import models
from django.contrib.auth.models import User


class Unite(models.Model):
    NOM_SITE_CHOICE = [
        ('Siège_RPC','Siège_RPC'),
        ('DIV_DEV','DIV_DEV'),
        ('DIV_RAF','DIV_RAF'),
        ('RA1K','RA1K'),
        ('RA2K','RA2K'),
        ('RA1Z','RA1Z'),
        ('RA1G','RA1G'),
        ('RA1D','RA1D'),
        ('CP2K','CP2K'),
        ('CP1Z','CP1Z'),
        ('PEC_Siège','PEC_Siège'),

    ]


    id_site = models.AutoField(primary_key=True)
    nom_site = models.CharField(max_length=50, choices=NOM_SITE_CHOICE)
    # Relation avec les utilisateurs Django (Many-to-Many)
    users = models.ManyToManyField(User, related_name='unites', blank=True)

    def __str__(self):
        return self.nom_site


class JuridiqueFournisseur(models.Model):
    # Choix pour les champs enum
    ETAT_CHOICES = [
        ('ACTIF', 'Actif'),
        ('BLACKLISTE', 'Blacklisté'),
        ('INACTIF', 'Inactif'),
    ]

    TYPE_CHOICES = [
        ('DEFINITIF', 'Definitif'),
        ('TEMPORAIRE', 'Temporaire'),
    ]

    TYPE_PARTENAIRE_CHOICES = [
        ('APPEL_D_OFFRE', 'Appel_d_offre'),
        ('AUTRE', 'Contrat_de_Fourniture"'),
    ]

    id = models.AutoField(primary_key=True)
    nom_du_contractant = models.CharField(max_length=255)
    num_fixe = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    nif = models.CharField(max_length=50, blank=True, null=True)
    date_exclusion = models.DateField(blank=True, null=True)
    duree_exclusion = models.IntegerField(blank=True, null=True)
    date_levee_sanction = models.DateField(blank=True, null=True)
    etat = models.CharField(max_length=50, choices=ETAT_CHOICES)  # etat du fournisseur blackliste ou pas
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)  # type blacklist definitif ou temporaire
    structure_ayant_exclu = models.CharField(max_length=255, blank=True, null=True)
    motifs = models.TextField(blank=True, null=True)
    remarques = models.TextField(blank=True, null=True)
    activite = models.CharField(max_length=255, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    code_postal = models.CharField(max_length=20, blank=True, null=True)
    wilaya = models.CharField(max_length=100, blank=True, null=True)
    n_identification_fiscale = models.CharField(max_length=100, blank=True, null=True)
    n_identification_statistique = models.CharField(max_length=100, blank=True, null=True)
    n_registre_commerce = models.CharField(max_length=100, blank=True, null=True)
    article_imposition = models.CharField(max_length=100, blank=True, null=True)
    systeme_numerotation_universel = models.CharField(max_length=100, blank=True, null=True)
    carte_artisant = models.CharField(max_length=100, blank=True, null=True)
    num_agrement = models.CharField(max_length=100, blank=True, null=True)
    crit_rech_1 = models.CharField(max_length=100, blank=True, null=True)
    rue = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=50, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    telephone_2 = models.CharField(max_length=20, blank=True, null=True)
    forme_juridique = models.CharField(max_length=100, blank=True, null=True)
    branche = models.CharField(max_length=100, blank=True, null=True)
    type_partenaire = models.CharField(max_length=100, blank=True, null=True, choices=TYPE_PARTENAIRE_CHOICES)
    cle_pays_banque = models.CharField(max_length=10, blank=True, null=True)
    cle_bancaire = models.CharField(max_length=10, blank=True, null=True)
    compte_bancaire = models.CharField(max_length=50, blank=True, null=True)
    cle_controle_bancaire = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.nom_du_contractant


class Contrat(models.Model):
    id = models.AutoField(primary_key=True)
    reference = models.CharField(max_length=100, blank=True, null=True)  # Champ de référence optionnel

    # Relation essentielle
    fournisseur = models.ForeignKey(JuridiqueFournisseur, on_delete=models.CASCADE, related_name='contrats')

    def __str__(self):
        if self.reference:
            return f"Contrat {self.reference} - {self.fournisseur.nom_du_contractant}"
        return f"Contrat {self.id} - {self.fournisseur.nom_du_contractant}"


class EvaluationContrat(models.Model):
    # Modification pour utiliser une relation avec le contrat et le fournisseur
    contrat = models.ForeignKey(Contrat, on_delete=models.CASCADE, related_name='evaluations', null=True)
    contractant = models.CharField(max_length=255)
    ecoute_client = models.IntegerField()
    respect_delais_contrat = models.IntegerField()
    respect_des_autres_obligations = models.IntegerField()
    taux_conformite = models.FloatField()
    flexibilite = models.IntegerField()
    total_evaluation = models.IntegerField()
    remarque = models.TextField(blank=True, null=True)

    # Champ pour suivre qui a fait l'évaluation
    evaluateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='evaluations')
    date_evaluation = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Évaluation de {self.contrat} - {self.date_evaluation}"