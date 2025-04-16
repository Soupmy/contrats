"""
Ce fichier contient des fonctions d'aide pour les tests de notifications
"""

from fournisseurs.models import JuridiqueFournisseur

# Sauvegarde l'état original avant de l'appel à save()
def save_fournisseur_with_state_tracking(fournisseur, notify=True):
    """
    Sauvegarde un fournisseur en gardant une trace de son état précédent
    pour permettre aux signaux de fonctionner correctement.
    
    Args:
        fournisseur: L'instance de JuridiqueFournisseur à sauvegarder
        notify: Si False, aucune notification ne sera générée
    """
    if hasattr(fournisseur, 'pk') and fournisseur.pk is not None:
        # Récupérer l'instance originale de la base de données
        try:
            original = JuridiqueFournisseur.objects.get(pk=fournisseur.pk)
            fournisseur._previous_state = original.etat
        except JuridiqueFournisseur.DoesNotExist:
            fournisseur._previous_state = None
    
    # Si notify est False, indiquer qu'aucune notification ne doit être générée
    if not notify:
        fournisseur._skip_notification = True
    
    # Sauvegarder l'instance
    fournisseur.save()