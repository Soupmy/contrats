from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('contrats', contrats, name='contrats'),
    path('fournisseurs', fournisseurs, name='fournisseurs'),
    path('blacklists', blacklists, name='blacklists'),
]
