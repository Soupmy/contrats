from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from fournisseurs.models import JuridiqueFournisseur
from notifications.models import Notification
import logging

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=JuridiqueFournisseur)
def capture_previous_state(sender, instance, **kwargs):
    """Capture l'état précédent avant sauvegarde"""
    try:
        instance._previous_state = JuridiqueFournisseur.objects.get(pk=instance.pk).etat
    except JuridiqueFournisseur.DoesNotExist:
        instance._previous_state = None

@receiver(post_save, sender=JuridiqueFournisseur)
def handle_blacklist_changes(sender, instance, created, **kwargs):
    """Gère les notifications de changement d'état"""
    if created:
        return

    previous_state = getattr(instance, '_previous_state', None)
    current_state = instance.etat

    # Récupérer un utilisateur admin (à adapter selon votre logique)
    from django.contrib.auth import get_user_model
    User = get_user_model()
    admin_user = User.objects.filter(is_superuser=True).first()

    if not admin_user:
        return

    # Ajout à la blacklist
    if previous_state != 'BLACKLISTE' and current_state == 'BLACKLISTE':
        message = f"Le fournisseur {instance.nom_du_contractant} a été ajouté à la blacklist"
        if instance.motifs:
            message += f" pour cause de : {instance.motifs}"
        
        Notification.objects.create(
            utilisateur=admin_user,
            fournisseur=instance,
            type_notification='AJOUT_BLACKLIST',
            message=message
        )

    # Retrait de la blacklist
    elif previous_state == 'BLACKLISTE' and current_state != 'BLACKLISTE':
        message = f"Le fournisseur {instance.nom_du_contractant} a été retiré de la blacklist"
        Notification.objects.create(
            utilisateur=admin_user,
            fournisseur=instance,
            type_notification='RETRAIT_BLACKLIST',
            message=message
        )