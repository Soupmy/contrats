from django.db import models
from fournisseurs.models import JuridiqueFournisseur
from django.contrib.auth import get_user_model

User = get_user_model()
class Notification(models.Model):
    TYPE_CHOICES = [
        ('AJOUT_BLACKLIST', '🔴 Ajout blacklist'),
        ('RETRAIT_BLACKLIST', '🟢 Retrait blacklist'),
    ]
    utilisateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    fournisseur = models.ForeignKey(JuridiqueFournisseur, on_delete=models.CASCADE)
    type_notification = models.CharField(max_length=50, choices=TYPE_CHOICES)
    message = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    lue = models.BooleanField(default=False)

    def icon_html(self):
        if self.type_notification == 'AJOUT_BLACKLIST':
            return '🔴'
        return '🟢'