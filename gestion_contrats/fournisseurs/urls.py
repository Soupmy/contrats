from django.urls import path
from . import views
from .views import export_fournisseurs_excel, export_blacklist_excel

urlpatterns = [
    path('', views.fournisseurs_view, name='fournisseurs'),
    path('details/<int:fournisseur_id>/', views.fournisseurs_details, name='fournisseurs'),
    path('modifier/<int:id>/', views.modifier_fournisseur, name='modifier_fournisseur'),
    path('supprimer/<int:id>/', views.supprimer_fournisseur, name='supprimer_fournisseur'),
    path('export-fournisseurs/', export_fournisseurs_excel, name='export_fournisseurs'),
    
    path('blacklist/', views.blacklist_view, name='blacklist'),
    path('blacklist/add/', views.blacklister_fournisseur, name='blacklister_fournisseur'),
    path('blacklist/add/', views.blacklister_fournisseur, name='blacklister_fournisseur'),
    path('export-blacklist/', export_blacklist_excel, name='export_blacklists'),
]


