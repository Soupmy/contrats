from django.shortcuts import render

# Create your views here.

def fournisseurs_view(request):
    return render(request , 'fournisseurs/fournisseurs.html')


def blacklist_view(request):
    return render(request, 'fournisseurs/blacklist.html')