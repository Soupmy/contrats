from django.shortcuts import render, redirect, get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from .models import Contrat  
from .forms import ContratForm 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.db.models import DateField, ForeignKey
from django.db.models.fields.files import FieldFile

def home(request):
    """Vue pour la page d'accueil"""
    return render(request, 'contracts/home.html')

@login_required
def contrats(request):
    """Vue pour afficher la liste des contrats et traiter l'ajout"""
    contrats = Contrat.objects.all().order_by('-date_saisie_contract')
    form = ContratForm()
    context = {
        'contrats': contrats,
        'form': form
    }
    
    if request.method == 'POST':
        form = ContratForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('contrats')
    
    return render(request, 'contracts/contrats.html', context)


@login_required
def contrats_details(request, contrat_id):
    contrat = get_object_or_404(Contrat, id=contrat_id)

    field_values = {}

    for field in contrat._meta.fields:
        value = getattr(contrat, field.name)

        if isinstance(value, FieldFile):
            # Fichier : récupérer l'URL s'il existe
            field_values[field.name] = value.url if value else None

        elif isinstance(field, DateField):
            # Date : formater proprement
            field_values[field.name] = value.strftime('%Y-%m-%d') if value else None

        elif isinstance(field, ForeignKey):
            # ForeignKey : afficher l'id de la relation si possible
            field_values[field.name] = value.pk if value else None

        else:
            # Valeur classique
            field_values[field.name] = value

    return JsonResponse(field_values)


@login_required
def supprimer_contrat(request, id):
    contrat = get_object_or_404(Contrat, id=id)

    if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
        contrat.delete()
        return JsonResponse({'success': True})
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Pour l'affichage dans la popup de confirmation
        return JsonResponse({'contrat': str(contrat)})

    # Sinon, requête non valide
    return JsonResponse({'success': False, 'error': 'Requête invalide'})

@login_required
def modifier_contrat(request, id):
    contrat = get_object_or_404(Contrat, id=id)

    if request.method == 'POST' and request.POST.get('_method') == 'PUT':
        form = ContratForm(request.POST, instance=contrat)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})

    form = ContratForm(instance=contrat)
    return render(request, 'contracts/modifier_contrat_form.html', {'form': form})