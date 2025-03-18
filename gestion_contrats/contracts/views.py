from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request , 'contracts/home.html')

def contrats(request):
    return render(request , 'contracts/contrats.html')