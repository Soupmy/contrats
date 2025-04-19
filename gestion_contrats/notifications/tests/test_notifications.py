from django.test import TestCase
from django.contrib.auth import get_user_model
from fournisseurs.models import JuridiqueFournisseur
from notifications.models import Notification
from django.utils import timezone

User = get_user_model()

class NotificationSignalTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='admin', password='testpass123')
        cls.fournisseur_data = {
            'nom_du_contractant': 'Fournisseur Test',
            'etat': 'HABILITE',  # Défini ici une seule fois
            'motifs': 'Test de notification'
        }

    def test_notification_on_blacklist_add(self):
        fournisseur = JuridiqueFournisseur.objects.create(**self.fournisseur_data)
        
        # Modification vers BLACKLISTE
        fournisseur.etat = 'BLACKLISTE'
        fournisseur.save()  # Doit déclencher le signal
        
        self.assertEqual(Notification.objects.count(), 1)

    def test_notification_on_blacklist_remove(self):
        """Test notification quand on retire de la blacklist"""
        # First create a blacklisted supplier
        fournisseur = JuridiqueFournisseur.objects.create(
            nom_du_contractant='Fournisseur Test',
            etat='BLACKLISTE',  # Start with BLACKLISTE
            motifs='Test de notification'
        )
        
        # Now change to HABILITE (removing from blacklist)
        fournisseur.etat = 'HABILITE'
        fournisseur.save()
        
        notification = Notification.objects.last()
        
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(notification.type_notification, 'RETRAIT_BLACKLIST')
        self.assertIn('retiré de la blacklist', notification.message)

    def test_no_notification_on_unchanged_state(self):
        """Aucune notification si pas de changement d'état"""
        fournisseur = JuridiqueFournisseur.objects.create(**self.fournisseur_data)
        
        # Modification sans changer l'état
        fournisseur.nom_du_contractant = 'Nouveau nom'
        fournisseur.save()
        
        self.assertEqual(Notification.objects.count(), 0)

class NotificationModelTests(TestCase):
    def test_notification_icon(self):
        """Test l'icône selon le type de notification"""
        fournisseur = JuridiqueFournisseur.objects.create(
            nom_du_contractant='Test Icon',
            etat='HABILITE'
        )
        
        notification = Notification.objects.create(
            fournisseur=fournisseur,
            type_notification='AJOUT_BLACKLIST',
            message='Test'
        )
        
        self.assertEqual(notification.icon_html(), '🔴')


    def test_notification_on_blacklist_remove(self):
        fournisseur = JuridiqueFournisseur.objects.create(
            nom_du_contractant='Test Retrait',
            etat='BLACKLISTE',
            motifs='Test'
        )
        
        # Modification vers HABILITE
        fournisseur.etat = 'HABILITE'
        fournisseur.save()
        
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.type_notification, 'RETRAIT_BLACKLIST')
        self.assertIn('retiré de la blacklist', notification.message)