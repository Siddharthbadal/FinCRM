from django.urls import path, include
from . import views

urlpatterns = [
    
    path('', views.clients_list, name='clients_list'),
    path('<int:pk>/', views.clients_detail, name='clients_detail'),
    path('<int:pk>/delete/', views.delete_client, name='delete_client'),
    path('<int:pk>/edit/', views.edit_client, name='edit_client'),
    path('add/', views.add_client, name='add_client'),
    path('<int:pk>/add_comment/',views.clients_detail, name='client_add_comment' )
    
]