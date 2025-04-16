""""
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('contrats', contrats, name='contrats'),
]
"""
from django.urls import path
"""from . import views"""
from .views import *


urlpatterns = [
    path('', views.home, name='home'),
    path('contrats/', views.contrats, name='contrats'),
    path('contrats/details/<int:contrat_id>/', views.details_contrat, name='details_contrat'),
    path('contrats/modifier/<int:contrat_id>/', views.modifier_contrat, name='modifier_contrat'),
    path('contrats/supprimer/<int:contrat_id>/', views.supprimer_contrat, name='supprimer_contrat'),
]
