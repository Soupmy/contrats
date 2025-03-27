from django.shortcuts import render, redirect, get_object_or_404
from .models import JuridiqueFournisseur
from .forms import FournisseurForm
from django.http import JsonResponse

# Create your views here.
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


def fournisseurs_details(request, fournisseur_id):
    fournisseurs = get_object_or_404(JuridiqueFournisseur, id=fournisseur_id)
    field_values = {field.name: getattr(fournisseurs, field.name) for field in fournisseurs._meta.fields}
    return JsonResponse(field_values)



#def supprimer_fournisseur(request, id):
    fournisseur = get_object_or_404(JuridiqueFournisseur, id=id)
    if request.method == 'POST':
        fournisseur.delete()
        return redirect('fournisseurs')
    return render(request, 'fournisseurs/supprimer_fournisseur.html', {'fournisseur': fournisseur})



def modifier_fournisseur(request, id):
    fournisseur = get_object_or_404(JuridiqueFournisseur, id=id)
    if request.method == 'POST':
        form = FournisseurForm(request.POST, instance=fournisseur)
        if form.is_valid():
            form.save()
            return redirect('fournisseurs')
    else:
        form = FournisseurForm(instance=fournisseur)
    return render(request, 'fournisseurs/modifier_fournisseur_popup.html', {'form': form})



def blacklist_view(request):
    blacklisted_fournisseurs = JuridiqueFournisseur.objects.all()
    return render(request, 'fournisseurs/blacklist.html', {'fournisseurs': blacklisted_fournisseurs})
