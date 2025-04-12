from django.urls import path
from . import views

urlpatterns = [
    path('', views.fournisseurs_view, name='fournisseurs'),
    path('details/<int:fournisseur_id>/', views.fournisseurs_details, name='fournisseurs'),
    path('modifier/<int:id>/', views.modifier_fournisseur, name='modifier_fournisseur'),
    path('supprimer/<int:id>/', views.supprimer_fournisseur, name='supprimer_fournisseur'),

    
    path('blacklist/', views.blacklist_view, name='blacklist'),
    path('blacklist/add/', views.blacklister_fournisseur, name='blacklister_fournisseur'),
    path('blacklist/add/', views.blacklister_fournisseur, name='blacklister_fournisseur')
]


