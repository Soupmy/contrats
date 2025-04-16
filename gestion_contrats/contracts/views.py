""""
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Contrat
from .forms import ContratForm

def home(request):
    return render(request , 'contracts/home.html')

def contrats(request):
    return render(request , 'contracts/contrats.html')

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Contrat
from .forms import ContratForm

def liste_contrats(request):
    contrats = Contrat.objects.all().order_by('-date_saisie_contract')
    return render(request, 'contracts/contrats.html', {'contrats': contrats})

def ajouter_contrat_popup(request):
    if request.method == 'POST':
        form = ContratForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('<script>window.close(); window.opener.location.reload();</script>')
    else:
        form = ContratForm()
    
    return render(request, 'contracts/ajouter_contrat_popup.html', {'form': form})
   
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Contrat
from .forms import ContratForm

def home(request):
    return render(request, 'contracts/home.html')

def contrats(request):
    contrats = Contrat.objects.all()
    form = ContratForm()
    context = {
        'contrats': contrats,
        'form': form
    }
    return render(request, 'contracts/contrats.html', context)

def ajouter_contrat(request):
    if request.method == 'POST':
        form = ContratForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ContratForm()
    return render(request, 'contracts/ajouter_contrat_popup.html', {'form': form})
    
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Contrat
from .forms import ContratForm
from gestion_contrats.contracts import models

def home(request):
    return render(request, 'contracts/home.html')

def contrats(request):
    contrats = Contrat.objects.all()
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
    
    return render(request,  'contracts/contrats.html', context)

def details_contrat(request, contrat_id):
    contrat = get_object_or_404(Contrat, id=contrat_id)
    
    # Obtenir toutes les valeurs du modèle de manière dynamique, pour éviter les erreurs
    contrat_data = {}
    
    # Ajouter tous les champs textuels
    for field in contrat._meta.fields:
        field_name = field.name
        
        # Récupérer la valeur du champ
        value = getattr(contrat, field_name)
        
        # Pour les champs avec des choix, récupérer la valeur affichable
        if field.choices and value:
            display_method = f"get_{field_name}_display"
            if hasattr(contrat, display_method):
                value = getattr(contrat, display_method)()
        
        # Pour les champs de relation, convertir en string
        if field.is_relation and value:
            value = str(value)
        
        # Pour les champs de fichier, afficher le nom du fichier s'il existe
        if isinstance(field, models.FileField) and value:
            value = value.name.split('/')[-1]  # Prendre juste le nom du fichier
            
        # Formater le nom du champ pour l'affichage
        display_name = field_name.replace('_', ' ').capitalize()
        
        contrat_data[display_name] = value
    
    return JsonResponse(contrat_data)

def modifier_contrat(request, contrat_id):
    contrat = get_object_or_404(Contrat, id=contrat_id)
    
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = ContratForm(request.POST, request.FILES, instance=contrat)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
    form = ContratForm(instance=contrat)
    return render(request, 'contracts/modifier_contrat_form.html', {'form': form})

def supprimer_contrat(request, contrat_id):
    contrat = get_object_or_404(Contrat, id=contrat_id)
    
    if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
        contrat.delete()
        return JsonResponse({'success': True})
    
    # Pour la requête GET, renvoyer le nom du contrat
    return JsonResponse({'contrat': contrat.intitul or f"Contrat #{contrat_id}"})
    """
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Contrat
from .forms import ContratForm

def home(request):
    """Vue pour la page d'accueil"""
    return render(request, 'contracts/home.html')

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

def details_contrat(request, contrat_id):
    """Vue pour obtenir les détails d'un contrat en format JSON"""
    contrat = get_object_or_404(Contrat, id=contrat_id)
    
    # Obtenir toutes les valeurs du modèle de manière dynamique
    contrat_data = {}
    
    # Ajouter tous les champs textuels
    for field in contrat._meta.fields:
        field_name = field.name
        
        # Récupérer la valeur du champ
        value = getattr(contrat, field_name)
        
        # Pour les champs avec des choix, récupérer la valeur affichable
        if hasattr(field, 'choices') and field.choices and value is not None:
            display_method = f"get_{field_name}_display"
            if hasattr(contrat, display_method):
                value = getattr(contrat, display_method)()
        
        # Pour les champs de relation, convertir en string
        if hasattr(field, 'is_relation') and field.is_relation and value is not None:
            value = str(value)
        
        # Pour les champs de fichier, afficher le nom du fichier s'il existe
        if str(field.__class__.__name__) == 'FileField' and value:
            value = value.name.split('/')[-1]  # Prendre juste le nom du fichier
            
        # Formater le nom du champ pour l'affichage
        display_name = field_name.replace('_', ' ').capitalize()
        
        contrat_data[display_name] = value
    
    return JsonResponse(contrat_data)

def modifier_contrat(request, contrat_id):
    """Vue pour modifier un contrat existant"""
    contrat = get_object_or_404(Contrat, id=contrat_id)
    
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = ContratForm(request.POST, request.FILES, instance=contrat)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
    form = ContratForm(instance=contrat)
    return render(request, 'contracts/modifier_contrat_form.html', {'form': form})

def supprimer_contrat(request, contrat_id):
    """Vue pour supprimer un contrat"""
    contrat = get_object_or_404(Contrat, id=contrat_id)
    
    if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
        contrat.delete()
        return JsonResponse({'success': True})
    
    # Pour la requête GET, renvoyer le nom du contrat
    return JsonResponse({'contrat': contrat.intitul or f"Contrat #{contrat_id}"})