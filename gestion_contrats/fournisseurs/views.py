from django.shortcuts import render, redirect, get_object_or_404
from .models import JuridiqueFournisseur
from .forms import FournisseurForm, BlacklistFournisseurForm
from django.http import JsonResponse
from django.contrib import messages
import datetime
from django.utils.dateparse import parse_date

# Create your views here.

# Affichage fournisseurs et ajout 
def fournisseurs_view(request):
    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fournisseurs')  # Redirige vers la même page après l'ajout
    else:
        form = FournisseurForm()
         
    fournisseurs = JuridiqueFournisseur.objects.all()
    return render(request, 'fournisseurs/fournisseurs.html', {'fournisseurs': fournisseurs, 'form': form})

# Affichage détails fournisseur en fonction de l'id
def fournisseurs_details(request, fournisseur_id):
    fournisseurs = get_object_or_404(JuridiqueFournisseur, id=fournisseur_id)
    field_values = {field.name: getattr(fournisseurs, field.name) for field in fournisseurs._meta.fields}
    return JsonResponse(field_values)



def supprimer_fournisseur(request, id):
    fournisseur = get_object_or_404(JuridiqueFournisseur, id=id)

    if request.method == 'POST'and request.POST.get('_method') == 'DELETE':
        fournisseur.delete()
        return JsonResponse({'success': True})
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'fournisseur': str(fournisseur)})

    # Sinon, requête non valide
    return JsonResponse({'success': False, 'error': 'Requête invalide'})
    





def modifier_fournisseur(request, id):
    fournisseur = get_object_or_404(JuridiqueFournisseur, id=id)

    if request.method == 'POST' and request.POST.get('_method') == 'PUT':
        form = FournisseurForm(request.POST, instance=fournisseur)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})

    form = FournisseurForm(instance=fournisseur)
    return render(request, 'fournisseurs/modifier_fournisseur_form.html', {'form': form})



def blacklist_view(request):
    filtre = request.GET.get('filtre', 'all')
    
    if filtre == 'temporaire':
        fournisseurs = JuridiqueFournisseur.objects.filter(
            etat='BLACKLISTE', 
            date_levee_sanction__isnull=False
        )
    elif filtre == 'a_vie':
        fournisseurs = JuridiqueFournisseur.objects.filter(
            etat='BLACKLISTE', 
            date_levee_sanction__isnull=True
        )
    else:  # 'all'
        fournisseurs = JuridiqueFournisseur.objects.filter(etat='BLACKLISTE')
    
    # Liste des fournisseurs qui ne sont pas encore blacklistés
    fournisseurs_disponibles = JuridiqueFournisseur.objects.filter(etat='HABILITE')
    
    context = {
        'fournisseurs': fournisseurs,
        'fournisseurs_disponibles': fournisseurs_disponibles,
    }
    
    return render(request, 'fournisseurs/blacklist.html', context)


def blacklister_fournisseur(request):
    if request.method == 'POST':
        # Debug avant validation
        print("Données POST reçues:", request.POST)
        
        # Récupérer le fournisseur directement depuis l'ID
        fournisseur_id = request.POST.get('fournisseur_id')
        if not fournisseur_id:
            messages.error(request, "Aucun fournisseur sélectionné")
            return redirect('blacklist')
            
        try:
            fournisseur = JuridiqueFournisseur.objects.get(id=fournisseur_id)
        except JuridiqueFournisseur.DoesNotExist:
            messages.error(request, "Fournisseur introuvable")
            return redirect('blacklist')
        
        # Appliquer les modifications
        fournisseur.etat = 'BLACKLISTE'
        fournisseur.structure_ayant_exclu = request.POST.get('structure_ayant_exclu', '')
        fournisseur.motifs = request.POST.get('motifs', '')
        fournisseur.remarques = request.POST.get('remarques', '')
        
        blacklist_type = request.POST.get('blacklist_type', 'temporaire')
        if blacklist_type == 'temporaire':
            fournisseur.date_exclusion = request.POST.get('date_exclusion')
            fournisseur.duree_exclusion = request.POST.get('duree_exclusion', '')
            fournisseur.date_levee_sanction = request.POST.get('date_levee_sanction')
        else:
            fournisseur.date_exclusion = datetime.date.today()
            fournisseur.duree_exclusion = 'Permanente'
            fournisseur.date_levee_sanction = None
        
        # Debug avant sauvegarde
        print("Fournisseur à sauvegarder:", {
            'nom': fournisseur.nom_du_contractant,
            'etat': fournisseur.etat,
            'date_exclusion': fournisseur.date_exclusion,
            'motifs': fournisseur.motifs
        })
        
        fournisseur.save()
        messages.success(request, f"Le fournisseur {fournisseur.nom_du_contractant} a été blacklisté avec succès.")
        return redirect('blacklist')
    
    messages.error(request, "Méthode non autorisée")
    return redirect('blacklist')