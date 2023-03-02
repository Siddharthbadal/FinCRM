
from django.urls import path, include
from dashboard.views import dashboard

app_name='dashboard'

urlpatterns = [
 

    path('', dashboard, name='index'),
    
]
