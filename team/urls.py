
from django.urls import path, include
from . import views 

urlpatterns = [
    path('<int:pk>/edit-team/',views.edit_team, name='edit_team')
]