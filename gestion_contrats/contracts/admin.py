from django.contrib import admin

# Register your models here.


from .models import JuridiqueFournisseur

admin.site.register(JuridiqueFournisseur)

from .models import EvaluationContrat

admin.site.register(EvaluationContrat)

from .models import Unite

admin.site.register(Unite)