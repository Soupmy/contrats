from django.urls import path
from . import views

urlpatterns = [
    path('fournisseurs/', views.fournisseurs_view, name='fournisseurs'),
    path('blacklist/', views.blacklist_view, name='blacklist'),
]