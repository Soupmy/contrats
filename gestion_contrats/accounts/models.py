# accounts/models.py
from django.db import models
from django.conf import settings  # <-- AJOUTER CET IMPORT MANQUANT
from django.contrib.auth.models import AbstractUser

class Unite(models.Model):
    id_site = models.AutoField(primary_key=True)
    nom_site = models.CharField(max_length=255)
    
    # Modification cruciale pour permettre NULL
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='unites_crees'
    )

    def __str__(self):
        return self.nom_site

class CustomUser(AbstractUser):
    unite = models.ForeignKey(
        Unite, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Unité"
    )