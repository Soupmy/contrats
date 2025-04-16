from django.test import TestCase
from django.core.management import call_command
from django.utils import timezone
from fournisseurs.models import JuridiqueFournisseur
from notifications.models import Notification

class UnblacklistCommandTests(TestCase):
    def test_unblacklist_scheduled(self):
        """Test la réhabilitation automatique des fournisseurs"""
        fournisseur = JuridiqueFournisseur.objects.create(
            nom_du_contractant='Test Auto',
            etat='BLACKLISTE',
            date_levee_sanction=timezone.now().date()
        )
        
        call_command('unblacklist_fournisseurs')
        
        fournisseur.refresh_from_db()
        notifications = Notification.objects.filter(fournisseur=fournisseur)
        
        self.assertEqual(fournisseur.etat, 'HABILITE')
        self.assertEqual(notifications.count(), 1)
        self.assertEqual(notifications[0].type_notification, 'RETRAIT_BLACKLIST')

class NotificationCommandTests(TestCase):
    def test_notification_command_output(self):
        """Test le output de la commande de notification"""
        JuridiqueFournisseur.objects.create(
            nom_du_contractant='Test Notif',
            etat='BLACKLISTE',
            date_levee_sanction=timezone.now().date() + timezone.timedelta(days=3)
        )
        
        with self.assertLogs('notification.management', level='INFO') as cm:
            call_command('notify_sanction_levee', '--jours-avant=3')
            
        self.assertIn("1 notifications envoyées", cm.output[0])