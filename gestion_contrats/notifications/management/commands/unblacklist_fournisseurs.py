from django.core.management.base import BaseCommand
from django.utils import timezone
from fournisseurs.models import JuridiqueFournisseur
from notifications.models import Notification

class Command(BaseCommand):
    help = 'Réhabilite automatiquement les fournisseurs dont la date de levée de sanction est dépassée'

    def handle(self, *args, **options):
        today = timezone.now().date()
        
        # Récupérer les fournisseurs dont la date de levée de sanction est passée et qui sont toujours blacklistés
        fournisseurs = JuridiqueFournisseur.objects.filter(
            date_levee_sanction__lte=today,
            etat='BLACKLISTE'  # Utiliser la bonne valeur d'état
        )
        
        count = 0
        for fournisseur in fournisseurs:
            # Sauvegarder l'état précédent avant modification
            fournisseur._previous_state = fournisseur.etat
            
            # Modifier l'état du fournisseur
            fournisseur.etat = 'HABILITE'  # Utiliser le bon état pour les fournisseurs réhabilités
            fournisseur.save()
            
            # La notification sera créée par le signal post_save
            count += 1
        
        self.stdout.write(self.style.SUCCESS(f'{count} fournisseurs ont été automatiquement réhabilités.'))