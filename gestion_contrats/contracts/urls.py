from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('contrats/', views.contrats, name='contrats'),
     path('details/<int:contrat_id>/', views.contrats_details, name='contrats_details'),
    path('modifier/<int:id>/', views.modifier_contrat, name='modifier_contrat'),
    path('supprimer/<int:id>/', views.supprimer_contrat, name='supprimer_contrat'),
    ]