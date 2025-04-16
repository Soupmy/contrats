from django.db import models
from fournisseurs.models import JuridiqueFournisseur

class Notification(models.Model):
    TYPE_CHOICES = [
        ('AJOUT_BLACKLIST', '🔴 Ajout blacklist'),
        ('RETRAIT_BLACKLIST', '🟢 Retrait blacklist'),
    ]
    
    fournisseur = models.ForeignKey(JuridiqueFournisseur, on_delete=models.CASCADE)
    type_notification = models.CharField(max_length=50, choices=TYPE_CHOICES)
    message = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    lue = models.BooleanField(default=False)

    def icon_html(self):
        if self.type_notification == 'AJOUT_BLACKLIST':
            return '🔴'
        return '🟢'