from django.core.management.base import BaseCommand
from django.utils import timezone
from fournisseurs.models import JuridiqueFournisseur
import logging

logger = logging.getLogger('notification.management')
class Command(BaseCommand):
    help = 'Notifie les levées de sanction à venir'

    def add_arguments(self, parser):
        parser.add_argument('--jours-avant', type=int, default=3)

    def handle(self, *args, **options):
        jours_avant = options['jours_avant']
        today = timezone.now().date()
        date_cible = today + timezone.timedelta(days=jours_avant)

        fournisseurs = JuridiqueFournisseur.objects.filter(
            date_levee_sanction=date_cible,
            etat='BLACKLISTE'
        )

        count = fournisseurs.count()
        logger.info(f"Nombre de fournisseurs trouvés : {count}")  # Log supplémentaire
        
        if count > 0:
            logger.info(f"{count} notifications créées pour les levées de sanction à venir.")
        else:
            logger.warning("Aucune notification à créer")