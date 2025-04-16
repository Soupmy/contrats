from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from fournisseurs.models import JuridiqueFournisseur
from notifications.models import Notification

class Command(BaseCommand):
    help = 'Envoie des notifications pour les fournisseurs dont la sanction sera levée dans un nombre de jours spécifié'

    def add_arguments(self, parser):
        parser.add_argument('--jours-avant', type=int, default=3, 
                           help='Nombre de jours avant la levée de sanction pour envoyer la notification')

    def handle(self, *args, **options):
        jours_avant = options['jours_avant']
        date_cible = timezone.now().date() + timedelta(days=jours_avant)
        
        # Récupérer les fournisseurs dont la date de levée de sanction est la date cible
        fournisseurs = JuridiqueFournisseur.objects.filter(
            date_levee_sanction=date_cible,
            etat='BLACKLISTE'  # Utiliser la bonne valeur d'état
        )
        
        count = 0
        for fournisseur in fournisseurs:
            Notification.objects.create(
                fournisseur=fournisseur,
                type_notification='SANCTION_LEVEE_PROCHE',
                message=f"La sanction du fournisseur {fournisseur.nom_du_contractant} sera levée dans {jours_avant} jours.",
                lue=False
            )
            count += 1
        
        self.stdout.write(self.style.SUCCESS(f'{count} notifications créées pour les levées de sanction à venir.'))