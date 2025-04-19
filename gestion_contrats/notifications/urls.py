from django.urls import path
from . import views

urlpatterns = [
    path('mark-as-read/<int:pk>/', views.mark_as_read, name='mark-as-read'),
    path('mark-all-read/', views.mark_all_read, name='mark-all-read'),
]