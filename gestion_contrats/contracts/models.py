from django.db import models
from fournisseurs.models import JuridiqueFournisseur
from django.db import models

def get_unite_model():
    from accounts.models import Unite
    return Unite
class Contrat(models.Model):
    # Identifiant unique du contrat
    id = models.AutoField(primary_key=True)

    # Fichiers liés au contrat
    dossier_consultation = models.FileField(upload_to='contrats/dossiers/', blank=True, null=True)
    pv_ouverture = models.FileField(upload_to='contrats/pv_ouverture/', blank=True, null=True)
    pv_attribution_prov_marche = models.FileField(upload_to='contrats/pv_attribution/', blank=True, null=True)
    copie_du_contrat = models.FileField(upload_to='contrats/copies/', blank=True, null=True)
    lettre_de_prolongation = models.FileField(upload_to='contrats/prolongations/', blank=True, null=True)
    lettre_invitation = models.FileField(upload_to='contrats/lettres_invitation/', blank=True, null=True)

    # Dates importantes
    date_prev_attrib_contrat = models.DateField(blank=True, null=True)
    date_prev_signat_contrat_bon = models.DateField(blank=True, null=True)
    date_reel_signat_contr_bon = models.DateField(blank=True, null=True)
    date_prev_notif_attribu = models.DateField(blank=True, null=True)
    date_reel_notif_attrib = models.DateField(blank=True, null=True)
    date_prev_signature_contrat = models.DateField(blank=True, null=True)
    date_reel_sign_cont = models.DateField(blank=True, null=True)
    date_exp_du_contrat = models.DateField(blank=True, null=True)
    date_saisie_contract = models.DateField(auto_now_add=True)  # Date du jour
    date_install_equip = models.DateField(blank=True, null=True)

    # Délais d'exécution
    delais_estimatif_execut_livrai = models.CharField(max_length=100, blank=True, null=True)
    delais_execution_livraison = models.CharField(max_length=100, blank=True, null=True)
    duree_contrat = models.CharField(max_length=100, blank=True, null=True)
    duree_attrib_contrat = models.CharField(max_length=100, blank=True, null=True)

    # Informations sur le contrat
    intitul = models.CharField(max_length=255, blank=True, null=True)
    nationalite = models.CharField(max_length=100, blank=True, null=True)
    nature = models.CharField(
        max_length=100,
        choices=[
            ('DAO', 'DAO'),
            ('passation', 'Passation'),
        ],
        blank=True,
        null=True,
        )
    typee = models.CharField(max_length=100, blank=True, null=True)
    type_du_contrat = models.CharField(
        max_length=100,
        choices=[
            ('fourniture', 'Fourniture'),
            ('travaux', 'Travaux'),
            ('services', 'Services'),
            ('etude_et_conseil', 'Étude et service de conseil'),
            ('prestation', 'Prestation'),
        ],
        blank=True,
        null=True,
    )
    filiale = models.CharField(max_length=100, blank=True, null=True)
    reference_du_contrat = models.CharField(
        max_length=100,
        choices=[
            ('oui', 'Oui'),
            ('non', 'Non'),
        ], 
        unique=True, 
        blank=True, 
        null=True,
        )
    la_monnai = models.CharField(max_length=50, blank=True, null=True)
    la_taxe = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    montant_contrat_devise = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    montant_contrat_da = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    recours = models.CharField(max_length=255, blank=True, null=True)

    # Relations avec d'autres modèles
    id_contractant = models.ForeignKey(JuridiqueFournisseur, on_delete=models.CASCADE, blank=True, null=True)
    unite = models.ForeignKey( get_unite_model(), on_delete=models.CASCADE )

    def __str__(self):
        return f"Contrat {self.reference_du_contrat} - {self.intitul}"