from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request , 'contracts/page1.html')

def contrats(request):
    return render(request , 'contracts/contrats.html')

def fournisseurs(request):
    return render(request , 'contracts/fournisseurs.html')

def blacklists(request):
    return render(request , 'contracts/blacklists.html')