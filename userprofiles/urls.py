from django.urls import path

from userprofiles.views import signup, myaccount
from django.contrib.auth import views

urlpatterns = [
   path('signup/', signup, name='signup'),
   path('log-in/', views.LoginView.as_view(template_name='userprofiles/login.html'), name='login'),
   path('logout/',views.LogoutView.as_view(), name='logout'),
   path('dashboard/myaacount/',myaccount, name='myaccount')

]