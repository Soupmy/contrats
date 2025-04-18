# Generated by Django 5.1.7 on 2025-03-11 22:50

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluationcontrat',
            name='id_fournisseur',
        ),
        migrations.AddField(
            model_name='evaluationcontrat',
            name='date_evaluation',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='evaluationcontrat',
            name='evaluateur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='evaluations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='unite',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='unites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='juridiquefournisseur',
            name='etat',
            field=models.CharField(choices=[('ACTIF', 'Actif'), ('BLACKLISTE', 'Blacklisté'), ('INACTIF', 'Inactif')], max_length=50),
        ),
        migrations.AlterField(
            model_name='juridiquefournisseur',
            name='type',
            field=models.CharField(choices=[('DEFINITIF', 'Definitif'), ('TEMPORAIRE', 'Temporaire')], max_length=50),
        ),
        migrations.AlterField(
            model_name='juridiquefournisseur',
            name='type_partenaire',
            field=models.CharField(blank=True, choices=[('APPEL_D_OFFRE', 'Appel_d_offre'), ('AUTRE', 'Contrat_de_Fourniture"')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='unite',
            name='nom_site',
            field=models.CharField(choices=[('Siège_RPC', 'Siège_RPC'), ('DIV_DEV', 'DIV_DEV'), ('DIV_RAF', 'DIV_RAF'), ('RA1K', 'RA1K'), ('RA2K', 'RA2K'), ('RA1Z', 'RA1Z'), ('RA1G', 'RA1G'), ('RA1D', 'RA1D'), ('CP2K', 'CP2K'), ('CP1Z', 'CP1Z'), ('PEC_Siège', 'PEC_Siège')], max_length=50),
        ),
        migrations.CreateModel(
            name='Contrat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('reference', models.CharField(blank=True, max_length=100, null=True)),
                ('fournisseur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contrats', to='contracts.juridiquefournisseur')),
            ],
        ),
        migrations.AddField(
            model_name='evaluationcontrat',
            name='contrat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to='contracts.contrat'),
        ),
    ]
