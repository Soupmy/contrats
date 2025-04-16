from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from fournisseurs.models import JuridiqueFournisseur  # Utiliser le bon nom de modèle
from notifications.models import Notification

@receiver(post_save, sender=JuridiqueFournisseur)
def notify_blacklist_changes(sender, instance, created, **kwargs):
    # Utiliser un flag pour déterminer si une notification doit être créée
    # Cette information doit être stockée dans une variable d'instance
    notification_created = getattr(instance, '_notification_created', False)
    
    if notification_created:
        # Éviter de créer des notifications supplémentaires
        return
    
    # Si c'est une modification (et non une création)
    if not created:
        # Retrouver l'état précédent (si possible)
        try:
            previous_state = getattr(instance, '_previous_state', None)
            current_state = instance.etat
            
            # Ajout à la blacklist
            if previous_state != 'BLACKLISTE' and current_state == 'BLACKLISTE':
                message = f"Le fournisseur {instance.nom_du_contractant} a été ajouté à la blacklist"
                if instance.motifs:
                    message += f" pour cause de : {instance.motifs}"
                
                Notification.objects.create(
                    fournisseur=instance,
                    type_notification='AJOUT_BLACKLIST',  # Utiliser le bon type
                    message=message,
                    lue=False
                )
                
                # Marquer que la notification a été créée
                instance._notification_created = True
            
            # Retrait de la blacklist
            elif previous_state == 'BLACKLISTE' and current_state != 'BLACKLISTE':
                message = f"Le fournisseur {instance.nom_du_contractant} a été retiré de la blacklist"
                
                Notification.objects.create(
                    fournisseur=instance,
                    type_notification='RETRAIT_BLACKLIST',  # Utiliser le bon type
                    message=message,
                    lue=False
                )
                
                # Marquer que la notification a été créée
                instance._notification_created = True
        
        except Exception as e:
            # En cas d'erreur, ne pas bloquer la sauvegarde
            pass