from django.shortcuts import render, redirect
from .models import JuridiqueFournisseur
from .forms import FournisseurForm

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



def blacklist_view(request):
    blacklisted_fournisseurs = JuridiqueFournisseur.objects.all()
    return render(request, 'fournisseurs/blacklist.html', {'fournisseurs': blacklisted_fournisseurs})