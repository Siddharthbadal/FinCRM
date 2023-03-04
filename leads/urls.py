from django.urls import path, include
from . import views

app_name = 'leads'


urlpatterns = [  
    path('', views.LeadListView.as_view(), name='list'),
    path("<int:pk>/", views.LeadDetailView.as_view(), name='detail'),
    path("<int:pk>/delete/", views.LeadDeleteView.as_view(), name='delete'),
    path("<int:pk>/edit/", views.LeadUpdateView.as_view(), name='edit'),
    path('add_lead/', views.LeadCreateView.as_view(), name='add_lead'),
    path('<int:pk>/convert/', views.ConvertToClient.as_view(), name='convert'), 
    path('<int:pk>/add-comment/', views.AddCommentView.as_view(), name='add_comment'),
    path('<int:pk>/add-file/',views.AddFileView.as_view(), name='add_file'),
    path('export/', views.client_export, name='lead_data_export'),
]