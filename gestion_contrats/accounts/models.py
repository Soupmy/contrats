from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Unite(models.Model):
    id_site = models.AutoField(primary_key=True)
    nom_site = models.CharField(max_length=255)

    def __str__(self):
        return self.nom_site
class CustomUser(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    unite = models.ForeignKey('Unite', on_delete=models.SET_NULL, null=True, blank=True)

    # Ajoutez des related_name uniques pour éviter les conflits
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_groups",  # Nom unique pour la relation inverse
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_permissions",  # Nom unique pour la relation inverse
        related_query_name="customuser",
    )

    def __str__(self):
        return self.username